console.log('JavaScript file loaded correctly');

window.onSpotifyWebPlaybackSDKReady = () => {
    if (typeof spotifyAccessToken === 'undefined' || !spotifyAccessToken) {
        console.log("Access token not available. Please login.");
        return;
    }

    // Initialize the Spotify Player
    const player = new Spotify.Player({
        name: 'Web Playback SDK',
        getOAuthToken: cb => {
            if (!spotifyRefreshToken) {
                console.error("No refresh token available");
                window.location.href = '/authorize/';
                return;
            }

            fetch('/refresh_token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ refresh_token: spotifyRefreshToken })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to refresh access token');
                }
                return response.json();
            })
            .then(data => {
                console.log("Token refreshed successfully");
                cb(data.access_token);
            })
            .catch(error => {
                console.error('Error fetching refreshed token:', error);
                window.location.href = '/authorize/';
            });
        },
        volume: 0.5
    });

    // Connect to the player
    player.connect().then(success => {
        if (success) {
            console.log('The Web Playback SDK successfully connected to Spotify!');
        } else {
            console.error('Failed to connect to Spotify Player');
        }
    }).catch(error => {
        console.error('Error connecting to Spotify Player:', error);
    });

    // Event handling for the player
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
        window.spotifyDeviceId = device_id;
        
        // Transfer playback to this device once it's ready
        transferPlayback(device_id).catch(error => {
            console.error('Error transferring playback:', error);
        });
    });

    player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
    });

    player.addListener('initialization_error', ({ message }) => {
        console.error('Failed to initialize:', message);
    });

    player.addListener('authentication_error', ({ message }) => {
        console.error('Failed to authenticate:', message);
        window.location.href = '/authorize/';
    });

    player.addListener('account_error', ({ message }) => {
        console.error('Failed to validate Spotify account:', message);
    });

    // Add play button functionality
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupPlayButtons);
    } else {
        setupPlayButtons();
    }

    // Function to transfer playback to current device
    async function transferPlayback(device_id) {
        try {
            const response = await fetch('/refresh_token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ refresh_token: spotifyRefreshToken })
            });

            if (!response.ok) throw new Error('Failed to refresh token');
            const data = await response.json();

            const transferResponse = await fetch('https://api.spotify.com/v1/me/player', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${data.access_token}`
                },
                body: JSON.stringify({
                    device_ids: [device_id],
                    play: false
                })
            });

            if (!transferResponse.ok && transferResponse.status !== 204) {
                throw new Error('Failed to transfer playback');
            }
        } catch (error) {
            console.error('Error transferring playback:', error);
        }
    }

    function setupPlayButtons() {
        const csrftoken = getCookie('csrftoken');
        document.querySelectorAll('.play-button').forEach(button => {
            button.addEventListener('click', async () => {
                const trackUri = button.getAttribute('data-track-uri');
                if (!trackUri) {
                    console.error('No track URI provided');
                    return;
                }

                if (!window.spotifyDeviceId) {
                    console.error('No device ID available');
                    return;
                }

                console.log('Attempting to play track:', trackUri);
                button.disabled = true;

                try {
                    const response = await fetch('/refresh_token/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({ refresh_token: spotifyRefreshToken })
                    });

                    if (!response.ok) throw new Error('Failed to refresh token');
                    const data = await response.json();

                    // First ensure our device is the active device
                    await transferPlayback(window.spotifyDeviceId);

                    // Then play the track
                    const playResponse = await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${window.spotifyDeviceId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${data.access_token}`
                        },
                        body: JSON.stringify({ uris: [trackUri] })
                    });

                    if (!playResponse.ok) {
                        const errorData = await playResponse.json();
                        throw new Error(`Failed to play track: ${errorData.error?.message || 'Unknown error'}`);
                    }

                    console.log('Playing track:', trackUri);

                    // Update button state/appearance if needed
                    button.textContent = 'Playing...';
                    setTimeout(() => {
                        button.textContent = 'Play';
                        button.disabled = false;
                    }, 1000);

                } catch (error) {
                    console.error('Error:', error);
                    button.disabled = false;
                    if (error.message.includes('Premium required')) {
                        alert('Spotify Premium is required to play tracks');
                    }
                }
            });
        });
    }
};

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}