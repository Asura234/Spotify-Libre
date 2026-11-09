# Nombres de los integrantes: José Ángel Aguirre López
#                             Eliseo Pedroza Juarez
#                             Angel Noe Navarro Contreras
#                             Emiliano Vazquez Castellanos
# Grupo: LIRD401
# Nombre del archivo: SpotyfyOriginal.py
# Descripcion: Spotify Pro | Master Edition

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import quote, unquote, parse_qs, urlparse
import json
import urllib.request

PAGINA_WEB = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spotify Pro | Master Edition</title>
    <link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: text; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #000; color: #fff; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        
        #authOverlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(18, 18, 18, 0.95); z-index: 999999; display: flex; justify-content: center; align-items: center;
            overflow-y: auto; padding: 20px; pointer-events: auto;
        }
        .auth-card {
            background: #181818; border: 1px solid #282828; padding: 30px; border-radius: 12px;
            width: 100%; max-width: 580px; display: flex; flex-direction: column; gap: 16px;
            box-shadow: 0 16px 32px rgba(0,0,0,0.8); position: relative; max-height: 95vh; overflow-y: auto;
            pointer-events: auto; z-index: 1000000;
        }
        .auth-header { display: flex; align-items: center; gap: 12px; font-weight: bold; font-size: 1.3rem; color: #fff; }
        .auth-header img { width: 36px; height: 36px; }
        .auth-group { display: flex; flex-direction: column; gap: 6px; pointer-events: auto; position: relative; z-index: 1000001; }
        .auth-group label { font-size: 0.85rem; color: #b3b3b3; font-weight: 600; cursor: pointer; }
        .auth-group input, .auth-group select {
            width: 100%; padding: 12px; background: #242424; border: 1px solid #444; border-radius: 8px;
            color: #fff; font-size: 0.95rem; outline: none; transition: border-color 0.2s; pointer-events: auto !important; position: relative; z-index: 1000002; cursor: text;
        }
        .auth-group input:focus, .auth-group select:focus { border-color: #1ed760; }
        .auth-group input:disabled { background: #121212; color: #777; border-color: #333; cursor: not-allowed; }
        
        .planes-grid { display: flex; flex-direction: column; gap: 10px; pointer-events: auto !important; z-index: 1000001; }
        .plan-option {
            background: #242424; border: 2px solid transparent; border-radius: 8px; padding: 12px;
            cursor: pointer; transition: all 0.2s; display: flex; flex-direction: column; gap: 4px; 
            pointer-events: auto !important; position: relative; z-index: 1000002;
        }
        .plan-option:hover { border-color: #666; background: #2a2a2a; }
        .plan-option.selected { border-color: #1ed760; background: #1f2c23; }
        .plan-title { font-weight: bold; font-size: 0.95rem; color: #fff; display: flex; justify-content: space-between; pointer-events: none; }
        .plan-desc { font-size: 0.78rem; color: #b3b3b3; line-height: 1.3; pointer-events: none; }

        .familiares-grid { display: grid; grid-template-columns: 1fr; gap: 10px; max-height: 260px; overflow-y: auto; padding-right: 4px; pointer-events: auto; }
        .familiar-box { background: #202020; padding: 10px; border-radius: 6px; border: 1px solid #333; display: flex; flex-direction: column; gap: 6px; pointer-events: auto; }
        .familiar-inputs-row { display: grid; grid-template-columns: 1.2fr 1.5fr 1.2fr; gap: 6px; }
        .familiar-box input { padding: 8px; font-size: 0.85rem; background: #121212; border: 1px solid #444; border-radius: 4px; color: #fff; pointer-events: auto !important; z-index: 1000002; cursor: text; }
        .familiar-box input:disabled { background: #181818; color: #888; border-color: #282828; cursor: not-allowed; }

        .btn-auth {
            background: #1ed760; color: #000; font-weight: bold; padding: 12px; border-radius: 25px;
            border: none; cursor: pointer; font-size: 1rem; transition: transform 0.2s; text-align: center; pointer-events: auto; z-index: 1000002;
        }
        .btn-auth:hover { transform: scale(1.02); background: #1fdf64; }
        .auth-switch { text-align: center; font-size: 0.85rem; color: #b3b3b3; cursor: pointer; pointer-events: auto; z-index: 1000002; }
        .auth-switch span { color: #1ed760; font-weight: bold; }
        .auth-switch span:hover { text-decoration: underline; }

        #spotifyToast {
            position: fixed; bottom: 100px; right: 30px; background-color: #1ed760; color: #000000;
            padding: 14px 24px; border-radius: 8px; font-weight: bold; font-size: 0.95rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6); display: flex; align-items: center; gap: 12px;
            z-index: 9999999; opacity: 0; transform: translateY(20px); transition: opacity 0.3s ease, transform 0.3s ease; pointer-events: none;
        }
        #spotifyToast.show { opacity: 1; transform: translateY(0); }

        #modalConfirmacionCustom {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85);
            display: none; justify-content: center; align-items: center; z-index: 1100000; pointer-events: auto;
        }
        .confirm-box {
            background: #1e1e1e; border: 1px solid #333; padding: 24px; border-radius: 12px; width: 400px;
            display: flex; flex-direction: column; gap: 18px; box-shadow: 0 16px 40px rgba(0,0,0,0.8); text-align: center;
        }

        .app-layout { display: grid; grid-template-columns: 280px 1fr; grid-template-rows: 1fr 90px; height: calc(100vh - 8px); gap: 8px; padding: 8px; }
        .sidebar { background-color: #121212; border-radius: 8px; display: flex; flex-direction: column; padding: 16px; gap: 16px; overflow-y: auto; }
        .sidebar-header { display: flex; justify-content: space-between; align-items: center; color: #b3b3b3; font-weight: bold; font-size: 0.95rem; }
        .sidebar-header span { display: flex; align-items: center; gap: 10px; cursor: pointer; }
        .btn-crear { background: none; border: none; color: #b3b3b3; font-size: 1.2rem; cursor: pointer; }
        .btn-crear:hover { color: #fff; }
        .library-actions { display: flex; gap: 8px; }
        .chip { background-color: #242424; color: #ffffff; border: none; padding: 6px 12px; border-radius: 16px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
        .chip:hover { background-color: #2a2a2a; }
        .playlist-list { display: flex; flex-direction: column; gap: 4px; }
        .playlist-item { padding: 10px; border-radius: 6px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: background 0.2s; }
        .playlist-item:hover { background-color: #1a1a1a; }
        .playlist-info { display: flex; flex-direction: column; gap: 2px; }
        .playlist-name { font-size: 0.9rem; font-weight: 500; }
        .playlist-owner { font-size: 0.75rem; color: #a7a7a7; }
        .playlist-actions-btn { display: flex; gap: 6px; }
        .btn-action-pl { background: none; border: none; color: #a7a7a7; cursor: pointer; font-size: 0.85rem; }
        .btn-action-pl:hover { color: #fff; }

        .main-content { background: #121212; border-radius: 8px; overflow-y: auto; display: flex; flex-direction: column; position: relative; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background-color: rgba(18, 18, 18, 0.95); backdrop-filter: blur(10px); padding: 12px 24px; z-index: 50; border-bottom: 1px solid #1f1f1f; }
        .nav-center-group { display: flex; align-items: center; gap: 12px; flex: 0 1 520px; }
        .home-btn { background-color: #242424; color: #fff; border: none; width: 48px; height: 48px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
        .home-btn:hover { transform: scale(1.05); background-color: #2a2a2a; }
        
        .search-container { flex: 1; position: relative; display: flex; align-items: center; }
        .search-container input { width: 100%; background-color: #242424; border: 1px solid transparent; border-radius: 500px; padding: 12px 40px 12px 45px; color: #fff; font-size: 0.95rem; outline: none; }
        .search-container input:focus { border-color: #fff; }
        .search-icon { position: absolute; left: 16px; color: #b3b3b3; }
        .search-clear { position: absolute; right: 16px; color: #b3b3b3; cursor: pointer; display: none; font-size: 1.1rem; }

        .search-dropdown { position: absolute; top: 56px; left: 0; width: 100%; background-color: #242424; border-radius: 8px; box-shadow: 0 16px 24px rgba(0,0,0,0.6); display: none; z-index: 100; max-height: 400px; overflow-y: auto; padding: 8px; }
        .dropdown-section-title { font-size: 0.75rem; color: #b3b3b3; padding: 8px 12px; font-weight: bold; }
        .history-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; border-radius: 4px; cursor: pointer; color: #fff; font-size: 0.9rem; }
        .history-item:hover { background-color: #333; }

        .user-profile { display: flex; align-items: center; gap: 10px; cursor: pointer; }
        .avatar { width: 32px; height: 32px; background-color: #1db954; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .content-body { padding: 16px 24px; display: flex; flex-direction: column; gap: 20px; overflow-y: auto; flex: 1; }

        .filter-chips { display: flex; gap: 8px; }
        .filter-chip { background-color: #2a2a2a; color: #fff; border: none; padding: 6px 14px; border-radius: 16px; font-size: 0.85rem; cursor: pointer; font-weight: 500; }
        .filter-chip.active, .filter-chip:hover { background-color: #fff; color: #000; }

        .playlist-header { display: flex; align-items: flex-end; gap: 24px; padding: 30px 24px; background: linear-gradient(to bottom, #2d5a88, #121212); border-radius: 8px; margin-top: 10px; }
        .playlist-header img { width: 150px; height: 150px; object-fit: cover; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-radius: 4px; }
        .playlist-header-meta h1 { font-size: 2.5rem; font-weight: bold; margin-top: 10px; }

        .songs-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.9rem; }
        .songs-table th { text-align: left; color: #b3b3b3; border-bottom: 1px solid #282828; padding-bottom: 10px; font-weight: normal; }
        .songs-table td { padding: 12px 8px; border-bottom: 1px solid #1f1f1f; color: #b3b3b3; }
        .songs-table tr:hover td { background-color: #ffffff10; color: #fff; }
        .song-title-cell { display: flex; align-items: center; gap: 12px; color: #fff; font-weight: 500; }
        .song-title-cell img { width: 40px; height: 40px; border-radius: 4px; object-fit: cover; }

        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; margin-top: 15px; }
        .card { background-color: #181818; padding: 12px; border-radius: 6px; cursor: pointer; transition: background 0.3s; display: flex; flex-direction: column; gap: 8px; position: relative; }
        .card:hover { background-color: #282828; }
        .card img { width: 100%; height: 150px; object-fit: cover; border-radius: 4px; }
        .card-title { font-weight: bold; font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .card-subtitle { font-size: 0.75rem; color: #a7a7a7; }

        .btn-dots { background: none; border: none; color: #b3b3b3; font-size: 1.2rem; cursor: pointer; padding: 4px 8px; }
        .btn-dots:hover { color: #fff; }

        .player-bar { grid-column: 1 / -1; background-color: #000; display: flex; justify-content: space-between; align-items: center; padding: 0 16px; height: 90px; border-top: 1px solid #282828; }
        .player-left { display: flex; align-items: center; gap: 14px; width: 30%; cursor: pointer; }
        .player-left img { width: 56px; height: 56px; border-radius: 4px; object-fit: cover; }
        .track-name { font-size: 0.9rem; font-weight: 500; }
        .track-artist { font-size: 0.75rem; color: #a7a7a7; }
        .player-center { display: flex; flex-direction: column; align-items: center; gap: 6px; width: 40%; }
        .player-controls { display: flex; align-items: center; gap: 20px; }
        
        .control-btn { background: none; border: none; color: #b3b3b3; cursor: pointer; font-size: 1.1rem; transition: color 0.2s; }
        .control-btn:hover { color: #fff; }
        .control-btn.active-blue { color: #1ed760; filter: drop-shadow(0 0 4px #1ed760); }

        .play-pause-btn { background-color: #fff; color: #000; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: none; cursor: pointer; }
        .btn-fav-player { background: none; border: none; color: #b3b3b3; font-size: 1.2rem; cursor: pointer; transition: color 0.2s; }
        .btn-fav-player:hover, .btn-fav-player.active { color: #1db954; }

        .playback-bar { display: flex; align-items: center; gap: 8px; width: 100%; max-width: 450px; font-size: 0.75rem; color: #a7a7a7; }
        .progress-slider { flex: 1; height: 4px; background: #4d4d4d; border-radius: 2px; appearance: none; accent-color: #1db954; cursor: pointer; }

        #nowPlayingOverlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(to bottom, #3b352b, #121212);
            z-index: 500; display: none; flex-direction: column; justify-content: space-between;
            padding: 24px; color: #fff; overflow-y: auto;
        }
        .np-header { display: flex; justify-content: space-between; align-items: center; }
        .np-header-btn { background: none; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; }
        .np-header-title { font-size: 0.8rem; font-weight: bold; text-align: center; text-transform: uppercase; color: #cccccc; }
        
        .np-cover-container { display: flex; justify-content: center; align-items: center; margin: 20px 0; position: relative; }
        .np-cover-img { width: 320px; height: 320px; border-radius: 8px; object-fit: cover; box-shadow: 0 16px 40px rgba(0,0,0,0.6); }
        
        .big-video-box {
            width: 380px; height: 260px; border-radius: 8px; overflow: hidden;
            box-shadow: 0 16px 40px rgba(0,0,0,0.8); position: relative; display: none;
            background: #000; border: 1px solid #333;
        }
        .btn-minimize-video {
            position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.7);
            color: #fff; border: none; width: 28px; height: 28px; border-radius: 50%;
            cursor: pointer; font-size: 1rem; font-weight: bold; display: flex;
            align-items: center; justify-content: center; z-index: 10;
        }
        .btn-minimize-video:hover { background: rgba(255,255,255,0.3); }

        .np-track-info { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 400px; margin: 0 auto; }
        .np-track-details h2 { font-size: 1.4rem; font-weight: bold; }
        .np-track-details p { color: #a7a7a7; font-size: 0.95rem; margin-top: 4px; }
        
        .np-btn-check {
            background: #1db954; color: #000; border: none;
            width: 28px; height: 28px; border-radius: 50%; font-weight: bold;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: all 0.2s ease;
        }
        .np-btn-check.desmarcado {
            background: transparent; color: #b3b3b3;
            border: 2px solid #b3b3b3;
        }
        .np-btn-check.desmarcado:hover {
            border-color: #fff; color: #fff;
        }

        .np-controls-container { width: 100%; max-width: 400px; margin: 0 auto; display: flex; flex-direction: column; gap: 15px; }
        .np-progress-group { display: flex; flex-direction: column; gap: 6px; }
        .np-time-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: #a7a7a7; }
        .np-main-controls { display: flex; justify-content: space-between; align-items: center; }
        .np-play-btn { width: 64px; height: 64px; border-radius: 50%; background: #fff; color: #000; font-size: 1.8rem; display: flex; align-items: center; justify-content: center; border: none; cursor: pointer; }
        .np-bottom-bar { display: flex; justify-content: space-between; align-items: center; width: 100%; max-width: 400px; margin: 15px auto 0; }

        #queueOverlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.85); backdrop-filter: blur(10px);
            z-index: 600; display: none; flex-direction: column; padding: 24px; color: #fff;
        }
        .queue-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .queue-title { font-size: 1.5rem; font-weight: bold; }
        .queue-subtitle { color: #a7a7a7; font-size: 0.85rem; margin-top: 4px; }
        .queue-list { display: flex; flex-direction: column; gap: 10px; overflow-y: auto; flex: 1; padding-right: 8px; }
        .queue-item { display: flex; align-items: center; justify-content: space-between; padding: 10px; background: #181818; border-radius: 6px; cursor: grab; }
        .queue-item.dragging { opacity: 0.5; background: #282828; }
        .queue-item-left { display: flex; align-items: center; gap: 12px; flex: 1; overflow: hidden; }
        .queue-item-left img { width: 48px; height: 48px; border-radius: 4px; object-fit: cover; }
        .queue-item-info { display: flex; flex-direction: column; gap: 2px; overflow: hidden; }
        .queue-item-name { font-size: 0.95rem; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .queue-item-artist { font-size: 0.8rem; color: #a7a7a7; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .queue-drag-handle { color: #b3b3b3; font-size: 1.2rem; cursor: grab; padding: 8px; }

        .context-menu { position: fixed; background: #282828; border-radius: 6px; padding: 6px; width: 220px; box-shadow: 0 10px 25px rgba(0,0,0,0.7); display: none; z-index: 200; font-size: 0.85rem; }
        .context-item { padding: 10px 12px; border-radius: 4px; cursor: pointer; display: flex; justify-content: space-between; color: #b3b3b3; }
        .context-item:hover { background: #3e3e3e; color: #fff; }

        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: none; justify-content: center; align-items: center; z-index: 300; }
        .modal-box { background: #282828; padding: 24px; border-radius: 12px; width: 460px; display: flex; flex-direction: column; gap: 16px; box-shadow: 0 16px 32px rgba(0,0,0,0.8); border: 1px solid #333; max-height: 90vh; overflow-y: auto; }
        .modal-header { display: flex; align-items: center; gap: 10px; font-weight: bold; font-size: 1.1rem; color: #fff; }
        .modal-header img { width: 26px; height: 26px; }
        .modal-box input, .modal-box select { width: 100%; padding: 12px; background: #121212; border: 1px solid #444; border-radius: 6px; color: #fff; font-size: 0.95rem; outline: none; }
        .modal-box input:focus, .modal-box select:focus { border-color: #1ed760; }
        .modal-buttons { display: flex; justify-content: flex-end; gap: 12px; margin-top: 5px; }
        .btn-modal { padding: 10px 20px; border-radius: 20px; font-weight: bold; border: none; cursor: pointer; font-size: 0.9rem; }
        .btn-modal:hover { transform: scale(1.03); }
        .btn-save { background: #1ed760; color: #000; }
        .btn-cancel { background: transparent; color: #b3b3b3; }
        .btn-cancel:hover { color: #fff; }
        .btn-danger { background: #e91429; color: #fff; }
        .btn-danger:hover { background: #ff1f35; }

        #ytMiniPlayerContainer {
            position: fixed; bottom: 20px; left: 20px; width: 160px; height: 90px;
            z-index: 999; background: #000; border-radius: 6px; overflow: hidden;
            border: 1px solid #333; display: none; box-shadow: 0 10px 25px rgba(0,0,0,0.8);
        }
        .mini-video-controls { position: absolute; top: 4px; right: 4px; display: flex; gap: 4px; z-index: 10; }
        .btn-mini-control { background: rgba(0,0,0,0.7); color: #fff; border: none; width: 22px; height: 22px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; display: flex; align-items: center; justify-content: center; }
        .btn-mini-control:hover { background: rgba(255,255,255,0.3); }

        #ytPlayerEmbed { width: 100%; height: 100%; border: none; }
        .btn-toggle-video { background: none; border: none; color: #b3b3b3; cursor: pointer; font-size: 0.9rem; }
        .btn-toggle-video:hover { color: #fff; }

        #modalCodigoFlotante {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85);
            display: none; justify-content: center; align-items: center; z-index: 1200000; pointer-events: auto;
        }
        .modal-codigo-box {
            background: #181818; border: 1px solid #333; padding: 28px; border-radius: 12px; width: 380px;
            display: flex; flex-direction: column; gap: 16px; box-shadow: 0 16px 40px rgba(0,0,0,0.9); text-align: center;
        }
    </style>
</head>
<body>

    <!-- PANTALLA DE AUTENTICACIÓN / REGISTRO / PAGOS / RECUPERACIÓN / LOGIN -->
    <div id="authOverlay" style="display:flex;">
        <div class="auth-card" id="cardRegistro">
            <div class="auth-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloRegistroCard">Spotify Pro | Elige tu propio paquete</span>
            </div>
            
            <div class="auth-group">
                <label id="labelNombreRegistro" for="regNombre">Nombre completo:</label>
                <input type="text" id="regNombre" placeholder="Ej. José Ángel Aguirre" autocomplete="off">
            </div>
            <div class="auth-group">
                <label for="regCorreo">Correo electrónico (Gmail, Yahoo o Institucional):</label>
                <input type="email" id="regCorreo" placeholder="tucorreo@gmail.com" autocomplete="off" oninput="verificarCorreoInstitucional(this.value)">
            </div>
            <div class="auth-group">
                <label for="regPassword">Contraseña:</label>
                <input type="password" id="regPassword" placeholder="••••••••" autocomplete="off">
            </div>
            <div class="auth-group" id="grupoPlanesSelector">
                <label id="labelSelectorPlanesTitulo">Elige tu Plan / Paquete:</label>
                <div class="planes-grid" id="planesContainer">
                    <div class="plan-option selected" id="optIndividual" onclick="seleccionarPlan('Individual', 139, this)">
                        <div class="plan-title"><span>Individual</span><span>$139 MXN / mes</span></div>
                        <div class="plan-desc">1 cuenta Premium. Música sin anuncios y reproducción ilimitada.</div>
                    </div>
                    <div class="plan-option" id="optEstudiantes" onclick="seleccionarPlan('Estudiantes', 74, this)">
                        <div class="plan-title"><span>Estudiantes</span><span>$74 MXN / mes (1 Mes Gratis)</span></div>
                        <div class="plan-desc">Descuento especial para universitarios verificados con correo UT León.</div>
                    </div>
                    <div class="plan-option" id="optDuo" onclick="seleccionarPlan('Dúo', 189, this)">
                        <div class="plan-title"><span>Dúo</span><span>$189 MXN / mes</span></div>
                        <div class="plan-desc">2 cuentas Premium (Titular + 1 invitado) para personas bajo el mismo techo.</div>
                    </div>
                    <div class="plan-option" id="optFamiliar" onclick="seleccionarPlan('Familiar', 239, this)">
                        <div class="plan-title"><span>Familiar</span><span>$239 MXN / mes</span></div>
                        <div class="plan-desc">Hasta 6 cuentas Premium (Titular + 5 invitados) en el mismo domicilio + Spotify Kids.</div>
                    </div>
                </div>
            </div>

            <div id="camposFamiliares" style="display:none; flex-direction: column; gap: 8px;">
                <label style="font-size: 0.85rem; color: #1ed760; font-weight: bold;" id="labelTituloMiembros">Registra a los Miembros:</label>
                <div class="familiares-grid" id="grid6Familiares"></div>
            </div>

            <button class="btn-auth" onclick="procesarContinuarPago()">Continuar con el pago</button>
            <div class="auth-switch" id="switchModoLogin" onclick="cambiarAModoLogin()">¿Ya tienes cuenta registrada? <span>Iniciar sesión</span></div>
        </div>

        <!-- TARJETA DE PAGO Y VERIFICACIÓN -->
        <div class="auth-card" id="cardPago" style="display:none;">
            <button onclick="cerrarTarjetaPago()" style="position:absolute; top:16px; right:16px; background:none; border:none; color:#b3b3b3; font-size:1.3rem; cursor:pointer;" title="Salir">✕</button>
            <div class="auth-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloPagoCard">Verificación de Pago por Correo</span>
            </div>
            
            <div style="background:#121212; padding:12px; border-radius:8px; border:1px solid #333; display:flex; flex-direction:column; gap:4px;">
                <div style="font-size:0.85rem; color:#1ed760; font-weight:bold;" id="resumenPlanNombre">Plan Seleccionado: Individual</div>
                <div style="font-size:0.8rem; color:#b3b3b3;" id="resumenPlanDesc">1 cuenta Premium. Música sin anuncios y reproducción ilimitada.</div>
                <div style="font-size:0.9rem; font-weight:bold; color:#fff; margin-top:4px;" id="resumenPlanPrecio">Total a pagar: $139 MXN / mes</div>
            </div>

            <div class="auth-group">
                <label for="inputCorreoVerificacion">Confirma tu correo para mandar el código:</label>
                <input type="email" id="inputCorreoVerificacion" placeholder="tucorreo@gmail.com" autocomplete="off">
            </div>

            <p style="font-size: 0.85rem; color: #b3b3b3;" id="textoPagoDesc">Haz clic para generar el código de verificación al correo ingresado.</p>

            <button class="btn-auth" style="background:#242424; color:#fff;" onclick="enviarCodigoServidorReal()">Mandar código de verificación al correo</button>
            
            <div class="auth-group">
                <label for="inputCodigoIngresado">Pega tu código de verificación de 6 dígitos:</label>
                <input type="text" id="inputCodigoIngresado" placeholder="Ej. 774877" maxlength="6" oninput="validarCodigoIngresado(this.value)">
            </div>

            <button class="btn-auth" id="btnAccederPlataforma" onclick="finalizarAccesoPlataforma()" disabled style="opacity: 0.4; cursor: not-allowed; background: #128038; color: #fff;">Acceder a la plataforma</button>
        </div>

        <!-- TARJETA REGISTRO DE INVITADOS / MIEMBROS DINÁMICO (TRAS CAMBIO DE PLAN A DÚO O FAMILIAR) -->
        <div class="auth-card" id="cardRegistroMiembroCambio" style="display:none;">
            <div class="auth-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloRegistroMiembroCambio">Registrar Invitados para Plan Compartido</span>
            </div>
            <p style="font-size: 0.85rem; color: #b3b3b3;" id="descRegistroMiembroCambio">Has cambiado a un plan compartido. Registra los datos de acceso para tus invitados:</p>
            
            <div id="contenedorGridInvitadosCambio" class="familiares-grid" style="max-height: 320px;"></div>

            <button class="btn-auth" style="margin-top: 8px;" onclick="guardarMiembroNuevoYFinalizar()">Guardar e ingresar a la plataforma</button>
        </div>

        <!-- TARJETA DE LOGIN / RENOVACIÓN DE PAQUETE PARA INVITADO EXPIRADO -->
        <div class="auth-card" id="cardLogin" style="display:none;">
            <div class="auth-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloLoginCard">Iniciar Sesión en Spotify Pro</span>
            </div>
            
            <div id="bannerInvitadoInfo" style="display:none; background:#1f2c23; border: 1px solid #1ed760; padding:12px; border-radius:8px; font-size:0.88rem; color:#fff; flex-direction: column; gap: 6px;">
                <div style="font-weight:bold; color:#1ed760;" id="tituloInvLoginDetalle">Invitación a Plan Compartido</div>
                <div id="textoInvLoginDetalle" style="font-size:0.82rem; color:#ccc;">Inicia sesión con tu cuenta existente para unirte automáticamente al plan compartido.</div>
            </div>

            <!-- CONTENEDOR DINÁMICO DE LOGIN O ELECCIÓN DE PLAN -->
            <div id="contenedorFormularioLogin">
                <div class="auth-group">
                    <label for="loginCorreo">Correo electrónico:</label>
                    <input type="email" id="loginCorreo" placeholder="tucorreo@gmail.com" autocomplete="off">
                </div>
                <div class="auth-group" style="margin-top: 10px;">
                    <label for="loginPassword">Contraseña:</label>
                    <input type="password" id="loginPassword" placeholder="••••••••" autocomplete="off">
                </div>
                <div style="display: flex; justify-content: flex-end; margin-top: 6px;">
                    <span onclick="mostrarOlvidoContrasena()" style="font-size: 0.8rem; color: #1ed760; cursor: pointer; font-weight: bold;">¿Se te olvidó la contraseña?</span>
                </div>
                <button class="btn-auth" style="margin-top: 16px; width:100%;" onclick="ejecutarLogin()">Iniciar Sesión</button>
            </div>

            <div class="auth-switch" id="switchCrearCuentaOpcion" onclick="cambiarAModoRegistro()">¿No tienes cuenta? <span>Crear una cuenta</span></div>
        </div>

        <!-- TARJETA REGISTRO INVITADA -->
        <div class="auth-card" id="cardRegistroInvitada" style="display:none;">
            <div class="auth-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloRegInv">Únete al plan compartido</span>
            </div>
            <div id="infoTitularInvTxt" style="background:#121212; padding:12px; border-radius:8px; font-size:0.88rem; color:#1ed760; font-weight:bold; border: 1px solid #333;"></div>
            <div class="auth-group">
                <label for="regInvNombre">Nombre completo:</label>
                <input type="text" id="regInvNombre" placeholder="Tu nombre..." autocomplete="off">
            </div>
            <div class="auth-group">
                <label for="regInvCorreo">Correo electrónico:</label>
                <input type="email" id="regInvCorreo" placeholder="tucorreo@gmail.com" autocomplete="off">
            </div>
            <div class="auth-group">
                <label for="regInvPassword">Crea tu contraseña:</label>
                <input type="password" id="regInvPassword" placeholder="••••••••" autocomplete="off">
            </div>
            <button class="btn-auth" onclick="finalizarRegistroInvitadaDirecto()">Aceptar Invitación y Acceder</button>
            <div class="auth-switch" onclick="cambiarLoginDesdeInvitada()">¿Ya estás registrado? <span>Iniciar sesión</span></div>
        </div>

        <!-- TARJETA RECUPERACIÓN DE CONTRASEÑA -->
        <div class="auth-card" id="cardOlvido" style="display:none;">
            <div class="auth-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span>Recuperar Contraseña (Titular o Invitado)</span>
            </div>
            <div class="auth-group">
                <label for="olvidoNombre">Nombre registrado:</label>
                <input type="text" id="olvidoNombre" placeholder="Ej. Juan Pérez">
            </div>
            <div class="auth-group">
                <label for="olvidoCorreo">Correo electrónico registrado:</label>
                <input type="email" id="olvidoCorreo" placeholder="tucorreo@gmail.com">
            </div>
            <button class="btn-auth" style="background:#242424; color:#fff;" onclick="enviarCodigoRecuperacion()">Verificar datos y enviar código</button>
            <div class="auth-group">
                <label for="olvidoCodigo">Código de verificación (6 dígitos):</label>
                <input type="text" id="olvidoCodigo" placeholder="Ej. 456789" maxlength="6">
            </div>
            <div class="auth-group">
                <label for="olvidoNuevaPass">Nueva contraseña:</label>
                <input type="password" id="olvidoNuevaPass" placeholder="Nueva contraseña">
            </div>
            <button class="btn-auth" onclick="ejecutarCambioPasswordOlvidada()">Actualizar Contraseña</button>
            <div class="auth-switch" onclick="volverDesdeOlvido()">← Regresar a Iniciar Sesión</div>
        </div>
    </div>

    <!-- MODAL DE VENTANA FLOTANTE PARA EL CÓDIGO DE VERIFICACIÓN -->
    <div id="modalCodigoFlotante">
        <div class="modal-codigo-box">
            <div style="font-weight:bold; font-size:1.1rem; color:#1ed760;">Código de Verificación</div>
            <div style="font-size:0.85rem; color:#b3b3b3;">Este código de 6 dígitos ha sido generado exitosamente.</div>
            <div id="textoCodigoFlotante" style="font-size:2rem; font-weight:bold; color:#1ed760; letter-spacing:6px; margin:10px 0;">159531</div>
            <button class="btn-auth" onclick="copiarCodigoYCerrarModal()">Copiar código y cerrar</button>
        </div>
    </div>

    <!-- MODAL CONFIRMACIÓN ESTILO SPOTIFY -->
    <div id="modalConfirmacionCustom">
        <div class="confirm-box">
            <div style="font-weight:bold; font-size:1.1rem; color:#1ed760;" id="tituloConfirmCustom">Confirmar acción</div>
            <div style="font-size:0.9rem; color:#b3b3b3;" id="textoConfirmCustom">¿Estás seguro de realizar esta acción?</div>
            <div style="display:flex; gap:10px; justify-content:center; margin-top:10px;">
                <button class="btn-modal btn-cancel" onclick="cerrarConfirmCustom(false)">No</button>
                <button class="btn-modal btn-save" id="btnConfirmCustomSi" onclick="cerrarConfirmCustom(true)">Sí, aceptar</button>
            </div>
        </div>
    </div>

    <!-- MODAL PARA MOSTRAR LINK DE INVITACIÓN -->
    <div class="modal-overlay" id="modalLinkInvitacion">
        <div class="modal-box">
            <div class="modal-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloModalInvitacion">Enlace de Invitación</span>
            </div>
            <p style="font-size:0.85rem; color:#b3b3b3;" id="textoDescInvitacion">Comparte este enlace con tu invitado para vincularlo directamente a tu plan compartido:</p>
            <div style="display:flex; gap:8px;">
                <input type="text" id="inputUrlInvitacion" readonly style="background:#121212; color:#1ed760; font-weight:bold;">
                <button class="btn-modal btn-save" onclick="copiarEnlaceInvitacion()">Copiar Link</button>
            </div>
            <div class="modal-buttons">
                <button class="btn-modal btn-save" onclick="document.getElementById('modalLinkInvitacion').style.display='none'; irAInicioApp();">Continuar a la Plataforma</button>
            </div>
        </div>
    </div>

    <!-- MODAL PARA CAMBIO DE CORREO ESTRICTO (SOLO CUANDO CAMBIA HACIA O DESDE PLAN ESTUDIANTES) -->
    <div class="modal-overlay" id="modalCambioCorreoPersonalizado">
        <div class="modal-box">
            <div class="modal-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span id="tituloModalCorreoPersonalizado">Actualización de Correo Requerida</span>
            </div>
            <p style="font-size:0.85rem; color:#b3b3b3;" id="descModalCorreoPersonalizado">Para cambiar de paquete, debes actualizar tu correo electrónico según corresponda:</p>
            <div class="auth-group">
                <label for="inputCorreoPersonalizadoNuevo" id="labelInputCorreoModal">Nuevo correo electrónico:</label>
                <input type="email" id="inputCorreoPersonalizadoNuevo" placeholder="tucorreo@gmail.com" autocomplete="off">
            </div>
            <div class="modal-buttons">
                <button class="btn-modal btn-cancel" onclick="document.getElementById('modalCambioCorreoPersonalizado').style.display='none'; document.getElementById('selectCambiarPaquete').value = sesionActiva.plan;">Cancelar</button>
                <button class="btn-modal btn-save" onclick="guardarCorreoPersonalizadoYContinuar()">Guardar y Continuar al Pago</button>
            </div>
        </div>
    </div>

    <!-- TOAST ESTILO SPOTIFY -->
    <div id="spotifyToast">
        <svg height="20" width="20" viewBox="0 0 24 24" fill="#000"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zm5.521 17.34c-.24.359-.732.48-1.091.24-2.985-1.826-6.741-2.241-11.157-1.229-.402.102-.804-.15-.906-.552-.102-.403.15-.804.552-.906 4.79-1.109 8.95-6.32 12.336-4.32.359.24.48.732.266 1.091zm1.47-3.875c-.301.459-.918.609-1.377.309-3.418-2.102-8.632-2.712-12.673-1.485-.512.155-1.053-.133-1.208-.644-.155-.512.133-1.053.644-1.208 4.607-1.398 10.354-.707 14.372 1.761.459.301.609.918.342 1.367zm.126-4.073c-4.102-2.437-10.87-2.662-14.792-1.463-.615.187-1.265-.162-1.452-.777-.187-.615.162-1.265.777-1.452 4.542-1.385 12.072-1.121 16.853 1.714.554.329.734 1.045.405 1.599-.329.554-1.045.734-1.591.379z"/></svg>
        <span id="toastMensaje">Acción realizada</span>
    </div>

    <!-- NOW PLAYING OVERLAY -->
    <div id="nowPlayingOverlay">
        <div class="np-header">
            <button class="np-header-btn" onclick="cerrarNowPlaying()">∨</button>
            <div>
                <div class="np-header-title" id="npHeaderCategory">REPRODUCIENDO DESDE BÚSQUEDA</div>
                <div style="font-weight: bold; text-align: center; font-size: 0.95rem;" id="npPlaylistTitle">Resultados</div>
            </div>
            <button class="np-header-btn" onclick="abrirMenuContextualActual(event)">⋮</button>
        </div>

        <div class="np-cover-container">
            <img id="npCoverImg" class="np-cover-img" src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=500" alt="Cover">
            <div id="bigVideoBox" class="big-video-box">
                <button class="btn-minimize-video" title="Minimizar video" onclick="minimizarVideoAGrande()">∨</button>
                <div id="bigVideoTarget" style="width:100%; height:100%;"></div>
            </div>
        </div>

        <div>
            <div class="np-track-info">
                <div class="np-track-details">
                    <h2 id="npTitle">Selecciona una pista</h2>
                    <p id="npArtist">Spotify Infinity</p>
                </div>
                <button class="np-btn-check" id="npCheckBtn" onclick="toggleFavoritoActual()">✓</button>
            </div>

            <div class="np-controls-container" style="margin-top: 20px;">
                <div class="np-progress-group">
                    <input type="range" class="progress-slider" id="npProgressSlider" value="0" min="0" max="100" oninput="cambiarProgreso(this.value)">
                    <div class="np-time-labels">
                        <span id="npCurrentTime">0:00</span>
                        <span id="npTotalTime">3:30</span>
                    </div>
                </div>

                <div class="np-main-controls">
                    <button class="control-btn" id="btnShuffleNP" onclick="toggleShuffle()">🔀</button>
                    <button class="control-btn" style="font-size: 1.8rem;" onclick="reproducirAnterior()">⏮</button>
                    <button class="np-play-btn" id="npPlayBtn" onclick="togglePlay()">▶</button>
                    <button class="control-btn" style="font-size: 1.8rem;" onclick="reproducirSiguiente()">⏭</button>
                    <button class="control-btn" id="btnRepeatNP" onclick="toggleRepeat()">🔁</button>
                </div>

                <div class="np-bottom-bar">
                    <button class="control-btn" title="Dispositivos">📱</button>
                    <div style="display: flex; gap: 20px;">
                        <button class="btn-toggle-video" onclick="accionBotonVerVideo()">📺 Ver video</button>
                        <button class="control-btn" title="Fila de reproducción" onclick="abrirQueueOverlay()">≡</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="queueOverlay">
        <div class="queue-header">
            <div>
                <div class="queue-title">Fila de reproducción</div>
                <div class="queue-subtitle" id="queueSubtitle">Resultados de Búsqueda</div>
            </div>
            <button class="btn-modal btn-cancel" style="font-size: 1.5rem;" onclick="cerrarQueueOverlay()">✕</button>
        </div>
        <div class="queue-list" id="queueContainer"></div>
    </div>

    <div class="app-layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <span onclick="irAInicio()">📚 Tu biblioteca</span>
                <button class="btn-crear" title="Crear Playlist" onclick="abrirModalPlaylist()">+</button>
            </div>
            <div class="library-actions">
                <button class="chip" onclick="verPlaylistsGuardadas()">Playlists</button>
                <button class="chip" onclick="verFavoritos()">Favoritos ⭐</button>
            </div>
            <div class="playlist-list" id="listaSidebar"></div>
        </aside>

        <main class="main-content" onclick="cerrarMenusGlobal(event)">
            <header class="top-bar">
                <button class="home-btn" onclick="irAInicio()" title="Inicio">🏠</button>
                <div class="nav-center-group">
                    <div class="search-container">
                        <span class="search-icon">🔍</span>
                        <input type="text" id="buscadorInput" placeholder="Busca cualquier artista, canción, álbum o podcast..." autocomplete="off" onfocus="mostrarDropdown()" oninput="manejarBusquedaInput(event)">
                        <span class="search-clear" id="searchClear" onclick="limpiarBusqueda()">✕</span>
                        
                        <div class="search-dropdown" id="searchDropdown">
                            <div class="dropdown-section-title">Búsquedas recientes</div>
                            <div id="listaHistorial"></div>
                        </div>
                    </div>
                </div>
                <div class="user-profile" onclick="abrirModalPerfil()">
                    <div class="avatar" id="avatarLetra">A</div>
                    <span id="nombreUsuarioLabel" style="font-size: 0.9rem; font-weight: 600;">Angel Aguirre</span>
                </div>
            </header>

            <div class="content-body" id="contenidoDinamico">
                <div class="filter-chips">
                    <button class="filter-chip active" onclick="filtrarTab('todo', this)">Todo</button>
                    <button class="filter-chip" onclick="filtrarTab('musica', this)">Música</button>
                    <button class="filter-chip" onclick="filtrarTab('podcasts', this)">Podcasts 🎙️</button>
                </div>

                <div id="vistaDinamica">
                    <section>
                        <h2 class="section-title" style="font-size: 1.3rem; margin-bottom: 12px;">Catálogo Mundial Infinito</h2>
                        <div class="cards-grid">
                            <div class="card" onclick="buscarDirecto('Santa Fe Klan')">
                                <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&auto=format&fit=crop&q=80" alt="Santa Fe Klan">
                                <div class="card-title">Santa Fe Klan</div>
                                <div class="card-subtitle">Todo el repertorio</div>
                            </div>
                            <div class="card" onclick="buscarDirecto('Luis Miguel')">
                                <img src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&auto=format&fit=crop&q=80" alt="Luis Miguel">
                                <div class="card-title">Luis Miguel</div>
                                <div class="card-subtitle">Discografía completa</div>
                            </div>
                            <div class="card" onclick="buscarDirecto('Podcast Exitosos')">
                                <img src="https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=300&auto=format&fit=crop&q=80" alt="Podcasts">
                                <div class="card-title">Podcasts Globales</div>
                                <div class="card-subtitle">Todos los programas y episodios</div>
                            </div>
                        </div>
                    </section>
                    <section style="margin-top: 25px;">
                        <h2 class="section-title" id="tituloResultados" style="font-size: 1.3rem; margin-bottom: 12px;">Resultados</h2>
                        <div id="mensajeEstado" style="color: #a7a7a7; font-size: 0.9rem; margin-bottom: 10px;">Busca cualquier artista, canción, álbum o podcast...</div>
                        <div id="gridResultados" class="cards-grid"></div>
                    </section>
                </div>
            </div>
        </main>

        <footer class="player-bar">
            <div class="player-left" onclick="abrirNowPlaying()">
                <img id="playerImg" src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=100&auto=format&fit=crop&q=80" alt="Cover">
                <div>
                    <div class="track-name" id="playerTitle">Selecciona una pista</div>
                    <div class="track-artist" id="playerArtist">Spotify Infinity</div>
                </div>
            </div>
            <div class="player-center">
                <div class="player-controls">
                    <button class="control-btn" id="btnShuffle" title="Reproducción Aleatoria" onclick="toggleShuffle()">🔀</button>
                    <button class="control-btn" title="Anterior" onclick="reproducirAnterior()">⏮</button>
                    <button class="play-pause-btn" id="playPauseBtn" onclick="togglePlay()">▶</button>
                    <button class="control-btn" title="Siguiente" onclick="reproducirSiguiente()">⏭</button>
                    <button class="btn-fav-player" id="playerFavBtn" title="Añadir a Tus Me Gusta" onclick="toggleFavoritoActual()">♥</button>
                    <button class="control-btn" id="btnRepeat" title="Repetir canción" onclick="toggleRepeat()">🔁</button>
                </div>
                <div class="playback-bar">
                    <span id="currentTime">0:00</span>
                    <input type="range" class="progress-slider" id="progressSlider" value="0" min="0" max="100" oninput="cambiarProgreso(this.value)">
                    <span id="totalTime">3:30</span>
                </div>
            </div>
            <div class="player-right">
                <button class="control-btn" title="Fila de reproducción" onclick="abrirQueueOverlay()">≡</button>
            </div>
        </footer>
    </div>

    <div id="ytMiniPlayerContainer">
        <div class="mini-video-controls">
            <button class="btn-mini-control" title="Ver en grande" onclick="agrandarVideoAPortada()">⛶</button>
            <button class="btn-mini-control" title="Cerrar video" onclick="cerrarVideoCompleto()">✕</button>
        </div>
        <div id="miniVideoTarget" style="width:100%; height:100%;">
            <iframe id="ytPlayerEmbed" src="" allow="autoplay; encrypted-media"></iframe>
        </div>
    </div>

    <div class="context-menu" id="contextMenu">
        <div class="context-item" onclick="reproducirDespues()">Reproducir en la fila ➔</div>
        <div class="context-item" onclick="abrirSubMenuPlaylists(event)">Mover a otra playlist ➔</div>
        <div class="context-item" onclick="agregarFavoritosDirecto()">Añadir a favoritos ❤️</div>
        <div class="context-item" style="color:#ff5555;" onclick="eliminarCancionActualContexto()">Eliminar elemento 🗑️</div>
    </div>

    <div class="context-menu" id="subMenuPlaylists" style="width: 200px;">
        <div style="padding: 6px 12px; font-weight: bold; color: #fff;">Elige la Playlist:</div>
        <div id="listaOpcionesPlaylists"></div>
    </div>

    <div class="modal-overlay" id="modalPlaylist">
        <div class="modal-box">
            <div class="modal-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span>Spotify Pro</span>
            </div>
            <h3 style="font-size: 1rem; color: #b3b3b3; font-weight: normal;">Nueva Playlist</h3>
            <input type="text" id="inputNombrePl" placeholder="Nombre de la playlist..." autocomplete="off">
            <div class="modal-buttons">
                <button class="btn-modal btn-cancel" onclick="cerrarModales()">Cancelar</button>
                <button class="btn-modal btn-save" onclick="crearPlaylist()">Crear</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="modalRenombrar">
        <div class="modal-box">
            <div class="modal-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span>Spotify Pro</span>
            </div>
            <h3 style="font-size: 1rem; color: #b3b3b3; font-weight: normal;">Nuevo nombre para la playlist:</h3>
            <input type="text" id="inputRenombrarPl" placeholder="Nuevo nombre..." autocomplete="off">
            <div class="modal-buttons">
                <button class="btn-modal btn-cancel" onclick="cerrarModales()">Cancelar</button>
                <button class="btn-modal btn-save" onclick="guardarRenombrarPlaylist()">Guardar</button>
            </div>
        </div>
    </div>

    <!-- MODAL DE PERFIL AMPLIADO -->
    <div class="modal-overlay" id="modalPerfil">
        <div class="modal-box">
            <div class="modal-header">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Logo">
                <span>Información de Perfil y Suscripción</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:8px; font-size:0.9rem; background:#121212; padding:12px; border-radius:6px;">
                <div><strong>Titular:</strong> <span id="perfilNombreLbl">Angel Aguirre</span></div>
                <div><strong>Correo:</strong> <span id="perfilCorreoLbl">correo@ejemplo.com</span></div>
                <div><strong>Paquete Actual:</strong> <span id="perfilPaqueteLbl" style="color:#1ed760; font-weight:bold;">Individual</span></div>
                <div><strong>Vigencia:</strong> <span id="perfilVigenciaLbl">Activo (1 mes)</span></div>
                
                <div style="background:#181818; padding:8px; border-radius:6px; border:1px solid #333; margin-top:4px;" id="contenedorCuposInv">
                    <div style="font-size:0.85rem; color:#1ed760; font-weight:bold;" id="txtCuposDisponibles">Cupos de Invitación: 0 / 5 usados</div>
                </div>

                <div style="border-top:1px solid #333; padding-top:6px; margin-top:4px;" id="contenedorSeccionMiembros">
                    <strong id="tituloSeccionMiembros">Miembros Vinculados:</strong>
                    <div id="perfilFamiliaresLista" style="font-size:0.8rem; color:#b3b3b3; margin-top:4px;">Ninguno</div>
                </div>

                <button class="btn-modal btn-save" style="margin-top:8px;" id="btnObtenerLinkPerfil" onclick="mostrarModalLinkInvitacionDirecto()">🔗 Obtener Enlace de Invitación</button>
            </div>

            <div style="background: #181818; padding: 12px; border-radius: 8px; border: 1px solid #333; display: flex; flex-direction: column; gap: 8px;">
                <div style="font-size: 0.9rem; font-weight: bold; color: #1ed760; cursor: pointer; display: flex; justify-content: space-between; align-items: center;" onclick="toggleMenuSeguridadPerfil()">
                    <span>🔐 Seguridad</span>
                    <span id="flechaSeguridad">▼</span>
                </div>
                <div id="contenedorSubmenuSeguridad" style="display: none; flex-direction: column; gap: 10px; margin-top: 6px; border-top: 1px solid #282828; padding-top: 8px;">
                    
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <label style="font-size: 0.8rem; color: #b3b3b3;">Ver Contraseña Actual:</label>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <input type="password" id="inputVerPassPerfil" readonly style="flex:1; background:#121212;">
                            <button class="btn-modal btn-cancel" style="padding: 8px;" onclick="toggleVerPasswordPerfilActual(this)" title="Ver / Ocultar">👁️</button>
                        </div>
                    </div>

                    <div style="border-top: 1px solid #282828; margin: 2px 0;"></div>

                    <div style="display: flex; flex-direction: column; gap: 6px;">
                        <label style="font-size: 0.8rem; color: #b3b3b3;">Cambiar Contraseña:</label>
                        <input type="password" id="perfilPassActual" placeholder="Contraseña actual" autocomplete="off">
                        <div style="display: flex; gap: 8px;">
                            <input type="password" id="perfilPassNueva1" placeholder="Nueva contraseña" autocomplete="off" style="flex:1;">
                            <input type="password" id="perfilPassNueva2" placeholder="Repetir nueva" autocomplete="off" style="flex:1;">
                        </div>
                        <button class="btn-modal btn-save" style="width: 100%; margin-top: 4px;" onclick="cambiarPasswordDesdePerfil()">Actualizar Contraseña</button>
                    </div>

                </div>
            </div>

            <div class="auth-group" id="grupoCambioPaquetePerfil" style="display: flex;">
                <label for="selectCambiarPaquete">Cambiar de Paquete / Renovar:</label>
                <select id="selectCambiarPaquete" onchange="iniciarCambioPaquete(this.value)">
                    <option value="Individual">Individual ($139 MXN)</option>
                    <option value="Estudiantes">Estudiantes ($74 MXN)</option>
                    <option value="Dúo">Dúo ($189 MXN)</option>
                    <option value="Familiar">Familiar ($239 MXN)</option>
                </select>
            </div>
            
            <div class="auth-group">
                <label for="inputNombrePerfil">Actualizar Nombre:</label>
                <input type="text" id="inputNombrePerfil" placeholder="Tu nombre..." autocomplete="off">
            </div>
            <div style="display:flex; gap:10px; margin-top:5px;">
                <button class="btn-modal btn-danger" style="flex:1;" onclick="confirmarCerrarSesion()">Cerrar sesión</button>
            </div>
            <div class="modal-buttons" style="margin-top:0;">
                <button class="btn-modal btn-cancel" onclick="cerrarModales()">Cerrar</button>
                <button class="btn-modal btn-save" onclick="guardarPerfil()">Guardar Cambios</button>
            </div>
        </div>
    </div>

    <script>
        let sesionActiva = JSON.parse(localStorage.getItem('sp_sesion_activa')) || null;
        let usuariosDB = JSON.parse(localStorage.getItem('sp_usuarios_db')) || [];
        let planSeleccionado = "Individual";
        let codigoGeneradoActual = "";
        let temporalRegistroData = null;
        let callbackConfirmCustom = null;
        let esModoInvitacion = false;
        let datosTitularInvitacion = null;
        let emailRecuperacionActual = "";
        let correoInvitadoOficialEnProceso = "";

        const infoPlanesData = {
            'Individual': { desc: '1 cuenta Premium. Música sin anuncios y reproducción ilimitada.', precio: '$139 MXN / mes' },
            'Estudiantes': { desc: 'Descuento especial para universitarios verificados con correo UT León (1 Mes Gratis).', precio: '$74 MXN / mes' },
            'Dúo': { desc: '2 cuentas Premium (Titular + 1 invitado) para personas bajo el mismo techo.', precio: '$189 MXN / mes' },
            'Familiar': { desc: 'Hasta 6 cuentas Premium (Titular + 5 invitados) en el mismo domicilio + Spotify Kids.', precio: '$239 MXN / mes' }
        };

        function validarDominioCorreo(correo) {
            const correoLower = correo.toLowerCase().trim();
            return correoLower.endsWith("@gmail.com") || 
                   correoLower.endsWith("@yahoo.com") || 
                   correoLower.endsWith("@alumnos.utleon.edu.mx");
        }

        function comprobarMembresiaInvitadoValida(usuario) {
            if (!usuario || !usuario.esInvitado) return true;
            let titularObj = usuariosDB.find(u => u.correo.toLowerCase() === usuario.titularAsociado.toLowerCase());
            if (!titularObj || (titularObj.plan !== 'Dúo' && titularObj.plan !== 'Familiar')) {
                return false;
            }
            let estaEnLista = titularObj.invitados && titularObj.invitados.some(inv => inv.correo.toLowerCase() === usuario.correo.toLowerCase());
            return estaEnLista;
        }

        window.addEventListener('storage', (e) => {
            if (e.key === 'sp_usuarios_db') {
                usuariosDB = JSON.parse(e.newValue) || [];
                if (sesionActiva && sesionActiva.esInvitado) {
                    if (!comprobarMembresiaInvitadoValida(sesionActiva)) {
                        mostrarToast("⚠️ El titular cambió de paquete. Tu membresía ha expirado.");
                        let correoGuardado = sesionActiva.correo;
                        localStorage.removeItem('sp_sesion_activa');
                        sesionActiva = null;
                        setTimeout(() => { 
                            document.getElementById('authOverlay').style.display = 'flex';
                            transformarTarjetaASeleccionPaqueteInvitado(correoGuardado);
                        }, 1000);
                    }
                }
            }
        });

        window.addEventListener('DOMContentLoaded', () => {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('invitacion') === 'true') {
                esModoInvitacion = true;
                datosTitularInvitacion = {
                    titular: urlParams.get('titular'),
                    correoTitular: urlParams.get('correo'),
                    plan: urlParams.get('plan')
                };
                
                document.getElementById('authOverlay').style.display = 'flex';
                document.getElementById('cardRegistro').style.display = 'none';
                document.getElementById('cardPago').style.display = 'none';
                document.getElementById('cardRegistroInvitada').style.display = 'none';
                document.getElementById('cardLogin').style.display = 'flex';
                
                document.getElementById('bannerInvitadoInfo').style.display = 'flex';
                document.getElementById('tituloInvLoginDetalle').textContent = `Invitación al plan ${datosTitularInvitacion.plan}`;
                document.getElementById('textoInvLoginDetalle').textContent = `${datosTitularInvitacion.titular} te ha invitado a su plan. Inicia sesión con la contraseña que te asignó el titular.`;
                document.getElementById('tituloLoginCard').textContent = "Inicia sesión con tus credenciales de invitado";
                return;
            }
            
            if (sesionActiva && sesionActiva.esInvitado) {
                if (!comprobarMembresiaInvitadoValida(sesionActiva)) {
                    let correoGuardado = sesionActiva.correo;
                    localStorage.removeItem('sp_sesion_activa');
                    sesionActiva = null;
                    document.getElementById('authOverlay').style.display = 'flex';
                    transformarTarjetaASeleccionPaqueteInvitado(correoGuardado);
                    return;
                }
            }

            if (!sesionActiva && !esModoInvitacion) {
                document.getElementById('authOverlay').style.display = 'flex';
                document.getElementById('cardRegistro').style.display = 'flex';
                document.getElementById('cardLogin').style.display = 'none';
                document.getElementById('cardPago').style.display = 'none';
            } else {
                document.getElementById('authOverlay').style.display = 'none';
                inicializarAppUsuario();
            }
        });

        function transformarTarjetaASeleccionPaqueteInvitado(correoInvitado = "") {
            correoInvitadoOficialEnProceso = correoInvitado;
            document.getElementById('cardRegistro').style.display = 'none';
            document.getElementById('cardPago').style.display = 'none';
            document.getElementById('cardOlvido').style.display = 'none';
            document.getElementById('cardRegistroInvitada').style.display = 'none';
            document.getElementById('cardLogin').style.display = 'flex';

            document.getElementById('tituloLoginCard').textContent = "Membresía Expirada - Elige tu Paquete o Regístrate";
            document.getElementById('bannerInvitadoInfo').style.display = 'flex';
            document.getElementById('bannerInvitadoInfo').style.background = '#381c1c';
            document.getElementById('bannerInvitadoInfo').style.borderColor = '#ff4d4d';
            document.getElementById('tituloInvLoginDetalle').textContent = "⚠️ Tu cuenta de invitado ya no está vinculada";
            document.getElementById('tituloInvLoginDetalle').style.color = '#ff4d4d';
            document.getElementById('textoInvLoginDetalle').textContent = "El titular del plan cambió de paquete. Si ya tienes cuenta registrada, ingresa tus datos correctos; de lo contrario, puedes crear una nueva cuenta abajo.";

            const contenedor = document.getElementById('contenedorFormularioLogin');
            contenedor.innerHTML = `
                <div class="auth-group">
                    <label for="invExpCorreo">Correo electrónico:</label>
                    <input type="email" id="invExpCorreo" value="${correoInvitado}" placeholder="tucorreo@gmail.com" autocomplete="off">
                </div>
                <div class="auth-group" style="margin-top:10px;">
                    <label for="invExpNombre">Nombre Completo:</label>
                    <input type="text" id="invExpNombre" placeholder="Tu nombre..." autocomplete="off">
                </div>
                <div class="auth-group" style="margin-top:10px;">
                    <label for="invExpPass">Contraseña:</label>
                    <input type="password" id="invExpPass" placeholder="••••••••" autocomplete="off">
                </div>

                <div class="auth-group" style="margin-top:12px;">
                    <label>Elige tu Paquete / Plan:</label>
                    <div class="planes-grid">
                        <div class="plan-option selected" id="optExpInd" onclick="seleccionarPlanExpirado('Individual', this)">
                            <div class="plan-title"><span>Individual</span><span>$139 MXN / mes</span></div>
                            <div class="plan-desc">1 cuenta Premium. Música sin anuncios y reproducción ilimitada.</div>
                        </div>
                        <div class="plan-option" id="optExpEst" onclick="seleccionarPlanExpirado('Estudiantes', this)">
                            <div class="plan-title"><span>Estudiantes</span><span>$74 MXN / mes (1 Mes Gratis)</span></div>
                            <div class="plan-desc">Descuento para universitarios verificados con correo UT León.</div>
                        </div>
                        <div class="plan-option" id="optExpDuo" onclick="seleccionarPlanExpirado('Dúo', this)">
                            <div class="plan-title"><span>Dúo</span><span>$189 MXN / mes</span></div>
                            <div class="plan-desc">2 cuentas Premium para personas bajo el mismo techo.</div>
                        </div>
                        <div class="plan-option" id="optExpFam" onclick="seleccionarPlanExpirado('Familiar', this)">
                            <div class="plan-title"><span>Familiar</span><span>$239 MXN / mes</span></div>
                            <div class="plan-desc">Hasta 6 cuentas Premium + Spotify Kids.</div>
                        </div>
                    </div>
                </div>

                <button class="btn-auth" style="margin-top: 16px; width:100%;" onclick="procesarPagoInvitadoExpirado()">Continuar con el pago del paquete</button>
            `;
            planSeleccionado = "Individual";
            document.getElementById('switchCrearCuentaOpcion').innerHTML = `¿No tienes cuenta registrada? <span onclick="cambiarAModoRegistro()">Crear una nueva cuenta desde cero</span>`;
        }

        function seleccionarPlanExpirado(plan, el) {
            planSeleccionado = plan;
            document.querySelectorAll('#contenedorFormularioLogin .plan-option').forEach(p => p.classList.remove('selected'));
            el.classList.add('selected');
        }

        function procesarPagoInvitadoExpirado() {
            const correo = document.getElementById('invExpCorreo').value.trim().toLowerCase();
            const nombre = document.getElementById('invExpNombre').value.trim();
            const password = document.getElementById('invExpPass').value.trim();

            if (!correo || !nombre || !password) {
                mostrarToast("⚠️ Todos los campos son obligatorios.");
                return;
            }

            if (!validarDominioCorreo(correo)) {
                mostrarToast("⚠️ Ingresa un correo electrónico válido (@gmail.com, @yahoo.com o institucional).");
                return;
            }

            let cuentaExistente = false;
            for (let u of usuariosDB) {
                if (u.correo.toLowerCase() === correo) {
                    cuentaExistente = true;
                    break;
                }
                if (u.invitados) {
                    let invMatch = u.invitados.find(i => i.correo.toLowerCase() === correo);
                    if (invMatch) {
                        cuentaExistente = true;
                        break;
                    }
                }
            }

            if (correoInvitadoOficialEnProceso && correo !== correoInvitadoOficialEnProceso.toLowerCase() && !cuentaExistente) {
                mostrarToast("❌ Error: Esta cuenta no está registrada en el sistema. Puedes crear una cuenta nueva.");
                return;
            }

            if (planSeleccionado === 'Estudiantes' && !correo.endsWith("@alumnos.utleon.edu.mx")) {
                mostrarToast("⚠️ El Plan Estudiantes requiere estrictamente tu correo institucional.");
                return;
            }

            temporalRegistroData = {
                nombre: nombre,
                correo: correo,
                password: password,
                plan: planSeleccionado,
                fechaRegistro: new Date().getTime(),
                invitados: [{ nombre: nombre, correo: correo, password: password }],
                esInvitado: false,
                titularAsociado: null
            };

            document.getElementById('cardLogin').style.display = 'none';
            document.getElementById('cardPago').style.display = 'flex';
            
            const inputCorreoVerif = document.getElementById('inputCorreoVerificacion');
            inputCorreoVerif.value = correo;
            inputCorreoVerif.disabled = true;

            document.getElementById('inputCodigoIngresado').value = '';

            const btnAcceder = document.getElementById('btnAccederPlataforma');
            btnAcceder.disabled = true;
            btnAcceder.style.opacity = '0.4';

            const infoP = infoPlanesData[planSeleccionado] || infoPlanesData['Individual'];
            document.getElementById('resumenPlanNombre').textContent = `Plan Seleccionado: ${planSeleccionado}`;
            document.getElementById('resumenPlanDesc').textContent = infoP.desc;
            document.getElementById('resumenPlanPrecio').textContent = `Total a pagar: ${infoP.precio}`;
            document.getElementById('textoPagoDesc').textContent = `Haz clic para mandar el código de verificación al correo oficial: ${correo}.`;
        }

        function ejecutarLogin() {
            const correo = document.getElementById('loginCorreo').value.trim().toLowerCase();
            const password = document.getElementById('loginPassword').value.trim();

            if (!correo || !password) {
                mostrarToast("⚠️ Todos los campos son obligatorios.");
                return;
            }

            let usuarioEncontrado = null;

            let userDirecto = usuariosDB.find(u => u.correo.toLowerCase() === correo);
            if (userDirecto) {
                if (userDirecto.password === password) {
                    usuarioEncontrado = userDirecto;
                } else {
                    mostrarToast("❌ Contraseña incorrecta. Si no estás registrado, crea una cuenta nueva.");
                    return;
                }
            } else {
                for (let u of usuariosDB) {
                    if (u.invitados) {
                        let invObj = u.invitados.find(i => i.correo.toLowerCase() === correo);
                        if (invObj) {
                            if (invObj.password === password) {
                                usuarioEncontrado = {
                                    nombre: invObj.nombre,
                                    correo: invObj.correo,
                                    password: invObj.password,
                                    plan: u.plan,
                                    fechaRegistro: u.fechaRegistro,
                                    esInvitado: true,
                                    titularAsociado: u.correo
                                };
                            } else {
                                mostrarToast("❌ Contraseña incorrecta para este invitado.");
                                return;
                            }
                            break;
                        }
                    }
                }
            }

            if (!usuarioEncontrado) {
                mostrarToast("❌ Error: Esta cuenta no está registrada en el sistema. Debes crear una cuenta nueva.");
                return;
            }

            if (usuarioEncontrado.esInvitado) {
                if (!comprobarMembresiaInvitadoValida(usuarioEncontrado)) {
                    transformarTarjetaASeleccionPaqueteInvitado(usuarioEncontrado.correo);
                    mostrarToast("⚠️ La membresía del titular expiró. Selecciona tu propio paquete.");
                    return;
                }
            }

            sesionActiva = usuarioEncontrado;
            
            // CARGAR PLAYLISTS Y FAVORITOS ASOCIADOS A ESTE CORREO DE FORMA SEGURA
            playlists = JSON.parse(localStorage.getItem('sp_pls_' + sesionActiva.correo)) || [];
            favoritos = JSON.parse(localStorage.getItem('sp_favs_' + sesionActiva.correo)) || [];

            localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));
            document.getElementById('authOverlay').style.display = 'none';
            inicializarAppUsuario();
            mostrarToast("Sesión iniciada correctamente.");
        }

        function finalizarRegistroInvitadaDirecto() {
            const nombre = document.getElementById('regInvNombre').value.trim();
            const correo = document.getElementById('regInvCorreo').value.trim().toLowerCase();
            const password = document.getElementById('regInvPassword').value.trim();

            if (!nombre || !correo || !password) {
                mostrarToast("Por favor completa todos los campos.");
                return;
            }

            if (!validarDominioCorreo(correo)) {
                mostrarToast("⚠️ Correo no válido. Solo @gmail.com, @yahoo.com o institucionales.");
                return;
            }

            let titObj = usuariosDB.find(u => u.correo === datosTitularInvitacion.correoTitular);
            if (titObj) {
                let limiteInvitados = titObj.plan === 'Dúo' ? 1 : (titObj.plan === 'Familiar' ? 5 : 0);
                let invitadosActuales = titObj.invitados ? titObj.invitados.filter(i => i.correo !== titObj.correo) : [];
                
                if (invitadosActuales.length >= limiteInvitados && !invitadosActuales.some(i => i.correo === correo)) {
                    mostrarToast(`⚠️ El plan ${titObj.plan} ya alcanzó su límite máximo de ${limiteInvitados} invitados.`);
                    return;
                }
            }

            let nuevoUsuarioInvitada = {
                nombre: nombre,
                correo: correo,
                password: password,
                plan: datosTitularInvitacion.plan,
                fechaRegistro: new Date().getTime(),
                invitados: [],
                esInvitado: true,
                titularAsociado: datosTitularInvitacion.correoTitular
            };

            sesionActiva = nuevoUsuarioInvitada;

            let idx = usuariosDB.findIndex(u => u.correo === sesionActiva.correo);
            if (idx >= 0) usuariosDB[idx] = sesionActiva;
            else usuariosDB.push(sesionActiva);

            if (titObj) {
                if (!titObj.invitados) titObj.invitados = [{ nombre: titObj.nombre, correo: titObj.correo, password: titObj.password }];
                if (!titObj.invitados.some(inv => inv.correo === sesionActiva.correo)) {
                    titObj.invitados.push({ nombre: sesionActiva.nombre, correo: sesionActiva.correo, password: sesionActiva.password });
                }
                let tIdx = usuariosDB.findIndex(u => u.correo === titObj.correo);
                if (tIdx >= 0) usuariosDB[tIdx] = titObj;
            }

            playlists = JSON.parse(localStorage.getItem('sp_pls_' + sesionActiva.correo)) || [];
            favoritos = JSON.parse(localStorage.getItem('sp_favs_' + sesionActiva.correo)) || [];
            localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
            localStorage.setItem('sp_favs_' + sesionActiva.correo, JSON.stringify(favoritos));

            localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));

            document.getElementById('authOverlay').style.display = 'none';
            inicializarAppUsuario();
            mostrarToast("¡Te has unido exitosamente al plan compartido!");
        }

        function cambiarLoginDesdeInvitada() {
            document.getElementById('cardRegistroInvitada').style.display = 'none';
            document.getElementById('cardLogin').style.display = 'flex';
            document.getElementById('bannerInvitadoInfo').style.display = 'flex';
            document.getElementById('tituloLoginCard').textContent = `Iniciar Sesión para unirte`;
            document.getElementById('switchCrearCuentaOpcion').style.display = 'block';
        }

        function verificarCorreoInstitucional(correo) {
            const esInstitucional = correo.toLowerCase().endsWith("@alumnos.utleon.edu.mx");
            
            const optIndividual = document.getElementById('optIndividual');
            const optEstudiantes = document.getElementById('optEstudiantes');
            const optDuo = document.getElementById('optDuo');
            const optFamiliar = document.getElementById('optFamiliar');
            const labelTitulo = document.getElementById('labelSelectorPlanesTitulo');

            if (esInstitucional) {
                optIndividual.style.display = 'none';
                optDuo.style.display = 'none';
                optFamiliar.style.display = 'none';
                
                optEstudiantes.style.display = 'flex';
                seleccionarPlan('Estudiantes', 74, optEstudiantes);
                labelTitulo.textContent = "Plan Detectado Automáticamente por Correo Institucional:";
                mostrarToast("🎓 ¡Correo institucional detectado! Plan de Estudiantes asignado automáticamente.");
            } else {
                optIndividual.style.display = 'flex';
                optEstudiantes.style.display = 'flex';
                optDuo.style.display = 'flex';
                optFamiliar.style.display = 'flex';
                labelTitulo.textContent = "Elige tu Plan / Paquete:";
            }
        }

        function actualizarGridMiembros(limite) {
            const grid = document.getElementById('grid6Familiares');
            grid.innerHTML = '';
            for(let i=1; i<=limite; i++) {
                if (i === 1) {
                    grid.innerHTML += `
                        <div class="familiar-box">
                            <div class="familiar-inputs-row">
                                <input type="text" id="famNombre1" value="Titular (Tú)" disabled>
                                <input type="email" id="famCorreo1" value="Tu correo registrado" disabled>
                                <input type="password" id="famPass1" value="Tu contraseña" disabled>
                            </div>
                        </div>
                    `;
                } else {
                    grid.innerHTML += `
                        <div class="familiar-box">
                            <div class="familiar-inputs-row">
                                <input type="text" id="famNombre${i}" placeholder="Nombre Invitado ${i-1}" autocomplete="off">
                                <input type="email" id="famCorreo${i}" placeholder="correo@gmail.com" autocomplete="off">
                                <input type="password" id="famPass${i}" placeholder="Contraseña" autocomplete="off">
                            </div>
                        </div>
                    `;
                }
            }
        }

        function mostrarToast(mensaje) {
            const toast = document.getElementById('spotifyToast');
            document.getElementById('toastMensaje').textContent = mensaje;
            toast.classList.add('show');
            setTimeout(() => { toast.classList.remove('show'); }, 3500);
        }

        function mostrarConfirmCustom(titulo, texto, callback, btnTexto = "Sí, aceptar") {
            document.getElementById('tituloConfirmCustom').textContent = titulo;
            document.getElementById('textoConfirmCustom').textContent = texto;
            document.getElementById('btnConfirmCustomSi').textContent = btnTexto;
            callbackConfirmCustom = callback;
            document.getElementById('modalConfirmacionCustom').style.display = 'flex';
        }

        function cerrarConfirmCustom(resultado) {
            document.getElementById('modalConfirmacionCustom').style.display = 'none';
            if (callbackConfirmCustom) callbackConfirmCustom(resultado);
        }

        function seleccionarPlan(nombrePlan, precio, elemento) {
            const correoVal = document.getElementById('regCorreo').value.trim().toLowerCase();
            if (correoVal.endsWith("@alumnos.utleon.edu.mx") && nombrePlan !== 'Estudiantes') {
                return;
            }

            planSeleccionado = nombrePlan;
            document.querySelectorAll('.plan-option').forEach(el => el.classList.remove('selected'));
            elemento.classList.add('selected');

            const camposFam = document.getElementById('camposFamiliares');
            const labelTit = document.getElementById('labelTituloMiembros');

            if (nombrePlan === 'Familiar' || nombrePlan === 'Dúo') {
                camposFam.style.display = 'flex';
                let limiteSlots = (nombrePlan === 'Familiar') ? 6 : 2;
                let maxInvitados = (nombrePlan === 'Familiar') ? 5 : 1;
                labelTit.textContent = `Registra a los Miembros y sus Contraseñas (${nombrePlan}: 1 Titular + ${maxInvitados} Invitados máx):`;
                actualizarGridMiembros(limiteSlots);
            } else {
                camposFam.style.display = 'none';
            }
        }

        function procesarContinuarPago() {
            const nombre = document.getElementById('regNombre').value.trim();
            const correo = document.getElementById('regCorreo').value.trim().toLowerCase();
            const password = document.getElementById('regPassword').value.trim();

            if (!nombre || !correo || !password) {
                mostrarToast("⚠️ Todos los campos del titular son obligatorios.");
                return;
            }

            if (!validarDominioCorreo(correo)) {
                mostrarToast("⚠️ Correo no válido. Solo @gmail.com, @yahoo.com o institucionales.");
                return;
            }

            let cuentaExistente = usuariosDB.find(u => u.correo.toLowerCase() === correo);
            if (!cuentaExistente) {
                for (let u of usuariosDB) {
                    if (u.invitados && u.invitados.find(i => i.correo.toLowerCase() === correo)) {
                        cuentaExistente = u;
                        break;
                    }
                }
            }

            if (cuentaExistente) {
                mostrarToast("⚠️ Esta cuenta ya está registrada. Redirigiendo a Iniciar Sesión...");
                setTimeout(() => {
                    cambiarAModoLogin();
                    document.getElementById('loginCorreo').value = correo;
                    document.getElementById('loginPassword').focus();
                }, 1500);
                return;
            }

            if (planSeleccionado === 'Estudiantes' && !correo.endsWith("@alumnos.utleon.edu.mx")) {
                mostrarToast("⚠️ Para el Plan Estudiantes es obligatorio ingresar tu correo institucional.");
                return;
            }

            let invitadosList = [{ nombre: nombre, correo: correo, password: password }];
            if (planSeleccionado === 'Familiar' || planSeleccionado === 'Dúo') {
                let limiteSlots = planSeleccionado === 'Familiar' ? 6 : 2;
                for(let i=2; i<=limiteSlots; i++) {
                    let n = document.getElementById(`famNombre${i}`).value.trim();
                    let c = document.getElementById(`famCorreo${i}`).value.trim().toLowerCase();
                    let p = document.getElementById(`famPass${i}`).value.trim();
                    if(n && c && p) {
                        if (!validarDominioCorreo(c)) {
                            mostrarToast(`⚠️ El correo del invitado ${n} no es válido.`);
                            return;
                        }
                        invitadosList.push({ nombre: n, correo: c, password: p });
                    }
                }
            }

            temporalRegistroData = {
                nombre, correo, password, plan: planSeleccionado,
                fechaRegistro: new Date().getTime(),
                invitados: invitadosList,
                esInvitado: false,
                titularAsociado: null
            };

            document.getElementById('cardRegistro').style.display = 'none';
            document.getElementById('cardPago').style.display = 'flex';
            document.getElementById('inputCorreoVerificacion').value = correo;
            document.getElementById('inputCodigoIngresado').value = '';

            const btnAcceder = document.getElementById('btnAccederPlataforma');
            btnAcceder.disabled = true;
            btnAcceder.style.opacity = '0.4';
            btnAcceder.style.cursor = 'not-allowed';

            const infoP = infoPlanesData[planSeleccionado] || infoPlanesData['Individual'];
            document.getElementById('resumenPlanNombre').textContent = `Plan Seleccionado: ${planSeleccionado}`;
            document.getElementById('resumenPlanDesc').textContent = infoP.desc;
            document.getElementById('resumenPlanPrecio').textContent = `Total a pagar: ${infoP.precio}`;
            document.getElementById('textoPagoDesc').textContent = `Haz clic para generar el código de verificación para ${correo}.`;
        }

        function cerrarTarjetaPago() {
            document.getElementById('cardPago').style.display = 'none';
            if (temporalRegistroData && temporalRegistroData.esCambioPlan) {
                document.getElementById('authOverlay').style.display = 'none';
            } else {
                document.getElementById('cardRegistro').style.display = 'flex';
            }
        }

        async function enviarCodigoServidorReal() {
            const correoIngresado = document.getElementById('inputCorreoVerificacion').value.trim() || document.getElementById('olvidoCorreo').value.trim();
            if (!correoIngresado || !correoIngresado.includes("@")) {
                mostrarToast("⚠️ Por favor ingresa un correo electrónico válido.");
                return;
            }

            try {
                const resp = await fetch("/api/enviar-codigo", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ correo: correoIngresado })
                });
                const data = await resp.json();
                if (data.success) {
                    codigoGeneradoActual = data.codigo;
                    document.getElementById('textoCodigoFlotante').textContent = codigoGeneradoActual;
                    document.getElementById('modalCodigoFlotante').style.display = 'flex';
                } else {
                    mostrarToast("Error al generar el código.");
                }
            } catch(e) {
                codigoGeneradoActual = Math.floor(100000 + Math.random() * 900000).toString();
                document.getElementById('textoCodigoFlotante').textContent = codigoGeneradoActual;
                document.getElementById('modalCodigoFlotante').style.display = 'flex';
            }
        }

        function copiarCodigoYCerrarModal() {
            navigator.clipboard.writeText(codigoGeneradoActual);
            document.getElementById('modalCodigoFlotante').style.display = 'none';
            
            if (document.getElementById('cardOlvido').style.display === 'flex') {
                document.getElementById('olvidoCodigo').value = codigoGeneradoActual;
            } else {
                document.getElementById('inputCodigoIngresado').value = codigoGeneradoActual;
                validarCodigoIngresado(codigoGeneradoActual);
            }
            mostrarToast("¡Código copiado y aplicado!");
        }

        function validarCodigoIngresado(valor) {
            const btnAcceder = document.getElementById('btnAccederPlataforma');
            if (valor === codigoGeneradoActual && codigoGeneradoActual.length === 6 && codigoGeneradoActual !== "") {
                btnAcceder.disabled = false;
                btnAcceder.style.opacity = '1';
                btnAcceder.style.cursor = 'pointer';
            } else {
                btnAcceder.disabled = true;
                btnAcceder.style.opacity = '0.4';
                btnAcceder.style.cursor = 'not-allowed';
            }
        }

        function finalizarAccesoPlataforma() {
            const codigoActualInput = document.getElementById('inputCodigoIngresado').value.trim();
            if (codigoActualInput !== codigoGeneradoActual || codigoGeneradoActual.length !== 6) {
                mostrarToast("⚠️ Debes introducir el código de verificación correcto para acceder.");
                return;
            }

            if (!temporalRegistroData) return;
            
            sesionActiva = temporalRegistroData;
            
            if (sesionActiva.plan === 'Individual' || sesionActiva.plan === 'Estudiantes') {
                sesionActiva.invitados = [{ nombre: sesionActiva.nombre, correo: sesionActiva.correo, password: sesionActiva.password }];
            }

            let idx = usuariosDB.findIndex(u => u.correo.toLowerCase() === sesionActiva.correo.toLowerCase());
            if (idx >= 0) usuariosDB[idx] = sesionActiva;
            else usuariosDB.push(sesionActiva);

            playlists = JSON.parse(localStorage.getItem('sp_pls_' + sesionActiva.correo)) || [];
            favoritos = JSON.parse(localStorage.getItem('sp_favs_' + sesionActiva.correo)) || [];
            localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
            localStorage.setItem('sp_favs_' + sesionActiva.correo, JSON.stringify(favoritos));

            localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));

            if (sesionActiva.esCambioPlan && (sesionActiva.plan === 'Dúo' || sesionActiva.plan === 'Familiar')) {
                document.getElementById('cardPago').style.display = 'none';
                document.getElementById('cardRegistroMiembroCambio').style.display = 'flex';
                
                const maxInv = sesionActiva.plan === 'Dúo' ? 1 : 5;
                document.getElementById('tituloRegistroMiembroCambio').textContent = `Registrar Invitados para Plan ${sesionActiva.plan}`;
                document.getElementById('descRegistroMiembroCambio').textContent = `Has actualizado a Plan ${sesionActiva.plan}. Ingresa los datos de hasta ${maxInv} invitado(s):`;
                
                const gridInv = document.getElementById('contenedorGridInvitadosCambio');
                gridInv.innerHTML = '';
                for (let i = 1; i <= maxInv; i++) {
                    gridInv.innerHTML += `
                        <div class="familiar-box" style="margin-bottom: 8px;">
                            <div style="font-size: 0.8rem; color: #1ed760; font-weight: bold; margin-bottom: 4px;">Invitado ${i}:</div>
                            <div class="auth-group">
                                <label style="font-size: 0.75rem;">Nombre completo:</label>
                                <input type="text" id="inputNombreInvNuevo${i}" placeholder="Ej. Invitado ${i}" autocomplete="off">
                            </div>
                            <div class="auth-group" style="margin-top: 4px;">
                                <label style="font-size: 0.75rem;">Correo electrónico:</label>
                                <input type="email" id="inputCorreoInvNuevo${i}" placeholder="invitado${i}@gmail.com" autocomplete="off">
                            </div>
                            <div class="auth-group" style="margin-top: 4px;">
                                <label style="font-size: 0.75rem;">Contraseña:</label>
                                <input type="password" id="inputPassInvNuevo${i}" placeholder="••••••••" autocomplete="off">
                            </div>
                        </div>
                    `;
                }
                
                mostrarToast("¡Pago verificado! Registra a tus nuevos invitados.");
                return;
            }

            document.getElementById('authOverlay').style.display = 'none';
            inicializarAppUsuario();
            mostrarToast("¡Pago verificado y cuenta configurada con éxito!");

            if (sesionActiva.plan === 'Individual' || sesionActiva.plan === 'Estudiantes') {
                localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            }
        }

        function guardarMiembroNuevoYFinalizar() {
            const maxInv = sesionActiva.plan === 'Dúo' ? 1 : 5;
            let nuevosInvitados = [{ nombre: sesionActiva.nombre, correo: sesionActiva.correo, password: sesionActiva.password }];

            for (let i = 1; i <= maxInv; i++) {
                const nom = document.getElementById(`inputNombreInvNuevo${i}`) ? document.getElementById(`inputNombreInvNuevo${i}`).value.trim() : "";
                const cor = document.getElementById(`inputCorreoInvNuevo${i}`) ? document.getElementById(`inputCorreoInvNuevo${i}`).value.trim().toLowerCase() : "";
                const pas = document.getElementById(`inputPassInvNuevo${i}`) ? document.getElementById(`inputPassInvNuevo${i}`).value.trim() : "";

                if (i === 1 && (!nom || !cor || !pas)) {
                    mostrarToast("⚠️ Debes ingresar al menos los datos del primer invitado.");
                    return;
                }

                if (nom && cor && pas) {
                    if (!validarDominioCorreo(cor)) {
                        mostrarToast(`⚠️ El correo del invitado ${i} no es válido.`);
                        return;
                    }
                    nuevosInvitados.push({ nombre: nom, correo: cor, password: pas });
                }
            }

            sesionActiva.invitados = nuevosInvitados;

            let idx = usuariosDB.findIndex(u => u.correo.toLowerCase() === sesionActiva.correo.toLowerCase());
            if (idx >= 0) usuariosDB[idx] = sesionActiva;

            localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));

            document.getElementById('cardRegistroMiembroCambio').style.display = 'none';
            document.getElementById('authOverlay').style.display = 'none';
            
            inicializarAppUsuario();
            desplegarModalLinkInvitacion();
            mostrarToast("¡Invitados guardados exitosamente!");
        }

        function desplegarModalLinkInvitacion() {
            if (!sesionActiva) return;
            let urlInvitacion = `${window.location.origin}/?invitacion=true&titular=${encodeURIComponent(sesionActiva.nombre)}&correo=${encodeURIComponent(sesionActiva.correo)}&plan=${encodeURIComponent(sesionActiva.plan)}`;
            document.getElementById('inputUrlInvitacion').value = urlInvitacion;
            let maxInv = sesionActiva.plan === 'Dúo' ? 1 : 5;
            document.getElementById('tituloModalInvitacion').textContent = `Enlace de Invitación - Plan ${sesionActiva.plan} (Máx ${maxInv} invitados)`;
            document.getElementById('modalLinkInvitacion').style.display = 'flex';
        }

        function mostrarModalLinkInvitacionDirecto() {
            cerrarModales();
            desplegarModalLinkInvitacion();
        }

        function copiarEnlaceInvitacion() {
            const inputUrl = document.getElementById('inputUrlInvitacion');
            navigator.clipboard.writeText(inputUrl.value);
            mostrarToast("¡Enlace de invitación copiado al portapapeles!");
        }

        function irAInicioApp() {
            inicializarAppUsuario();
            mostrarToast("¡Acceso autorizado a Spotify Pro!");
        }

        function cambiarAModoLogin() {
            document.getElementById('cardRegistro').style.display = 'none';
            document.getElementById('cardRegistroInvitada').style.display = 'none';
            document.getElementById('bannerInvitadoInfo').style.display = 'none';
            document.getElementById('cardLogin').style.display = 'flex';
            document.getElementById('tituloLoginCard').textContent = "Iniciar Sesión en Spotify Pro";
        }

        function cambiarAModoRegistro() {
            document.getElementById('cardLogin').style.display = 'none';
            document.getElementById('cardRegistro').style.display = 'flex';
            document.getElementById('regNombre').value = '';
            document.getElementById('regCorreo').value = '';
            document.getElementById('regPassword').value = '';
            document.getElementById('tituloRegistroCard').textContent = "Spotify Pro | Elige tu propio paquete";
        }

        function mostrarOlvidoContrasena() {
            document.getElementById('cardLogin').style.display = 'none';
            document.getElementById('cardOlvido').style.display = 'flex';
        }

        function volverDesdeOlvido() {
            document.getElementById('cardOlvido').style.display = 'none';
            document.getElementById('cardLogin').style.display = 'flex';
        }

        async function enviarCodigoRecuperacion() {
            const nombreInput = document.getElementById('olvidoNombre').value.trim();
            const correoInput = document.getElementById('olvidoCorreo').value.trim().toLowerCase();

            if (!nombreInput || !correoInput || !correoInput.includes("@")) {
                mostrarToast("⚠️ Ingresa el nombre y el correo electrónico registrado.");
                return;
            }

            let encontrado = false;
            for (let u of usuariosDB) {
                if (u.correo.toLowerCase() === correoInput && u.nombre.toLowerCase() === nombreInput.toLowerCase()) {
                    encontrado = true;
                    break;
                }
                if (u.invitados) {
                    let invMatch = u.invitados.find(inv => inv.correo.toLowerCase() === correoInput && inv.nombre.toLowerCase() === nombreInput.toLowerCase());
                    if (invMatch) {
                        encontrado = true;
                        break;
                    }
                }
            }

            if (!encontrado) {
                mostrarToast("❌ Error: Esta cuenta no está registrada en el sistema.");
                return;
            }

            emailRecuperacionActual = correoInput;
            await enviarCodigoServidorReal();
            mostrarToast("✅ Datos verificados. Código de recuperación enviado.");
        }

        function ejecutarCambioPasswordOlvidada() {
            const codigoInput = document.getElementById('olvidoCodigo').value.trim();
            const nuevaPass = document.getElementById('olvidoNuevaPass').value.trim();

            if (codigoInput !== codigoGeneradoActual || codigoGeneradoActual.length !== 6) {
                mostrarToast("⚠️ Código de verificación incorrecto.");
                return;
            }
            if (!nuevaPass) {
                mostrarToast("⚠️ Ingresa una contraseña nueva.");
                return;
            }

            let actualizado = false;
            for (let u of usuariosDB) {
                if (u.correo.toLowerCase() === emailRecuperacionActual.toLowerCase()) {
                    u.password = nuevaPass;
                    actualizado = true;
                }
                if (u.invitados) {
                    for (let inv of u.invitados) {
                        if (inv.correo.toLowerCase() === emailRecuperacionActual.toLowerCase()) {
                            inv.password = nuevaPass;
                            actualizado = true;
                        }
                    }
                }
            }

            if (actualizado) {
                localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
                if (sesionActiva && sesionActiva.correo.toLowerCase() === emailRecuperacionActual.toLowerCase()) {
                    sesionActiva.password = nuevaPass;
                    localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));
                }
                mostrarToast("¡Contraseña actualizada con éxito!");
                volverDesdeOlvido();
            } else {
                mostrarToast("Error al actualizar la contraseña.");
            }
        }

        function confirmarCerrarSesion() {
            cerrarModales();
            mostrarConfirmCustom(
                "Cerrar Sesión",
                "¿Estás seguro de que quieres cerrar sesión?",
                (aceptado) => {
                    if (aceptado) {
                        sesionActiva = null;
                        localStorage.removeItem('sp_sesion_activa');
                        document.getElementById('authOverlay').style.display = 'flex';
                        document.getElementById('cardRegistro').style.display = 'flex';
                        document.getElementById('cardLogin').style.display = 'none';
                        document.getElementById('cardPago').style.display = 'none';
                        mostrarToast("Sesión cerrada correctamente.");
                    }
                },
                "Sí, cerrar sesión"
            );
        }

        function inicializarAppUsuario() {
            if (sesionActiva) {
                usuario = sesionActiva.nombre; 
                document.getElementById('nombreUsuarioLabel').textContent = sesionActiva.nombre;
                document.getElementById('avatarLetra').textContent = sesionActiva.nombre.charAt(0).toUpperCase();
                document.getElementById('perfilNombreLbl').textContent = sesionActiva.nombre;
                document.getElementById('perfilCorreoLbl').textContent = sesionActiva.correo;
                document.getElementById('perfilPaqueteLbl').textContent = sesionActiva.plan || "Individual";
                
                // CARGAR PLAYLISTS Y FAVORITOS ASOCIADOS A ESTE USUARIO ACTIVO DE FORMA SEGURA
                playlists = JSON.parse(localStorage.getItem('sp_pls_' + sesionActiva.correo)) || [];
                favoritos = JSON.parse(localStorage.getItem('sp_favs_' + sesionActiva.correo)) || [];

                let famCont = document.getElementById('perfilFamiliaresLista');
                let tituloSec = document.getElementById('tituloSeccionMiembros');
                let grupoCambio = document.getElementById('grupoCambioPaquetePerfil');
                let txtCupos = document.getElementById('txtCuposDisponibles');
                let contenedorCupos = document.getElementById('contenedorCuposInv');
                let btnLinkPerfil = document.getElementById('btnObtenerLinkPerfil');

                grupoCambio.style.display = 'flex';

                if (sesionActiva.esInvitado && sesionActiva.titularAsociado) {
                    tituloSec.textContent = "Titular Asociado:";
                    famCont.textContent = sesionActiva.titularAsociado;
                    if (contenedorCupos) contenedorCupos.style.display = 'none';
                    if (btnLinkPerfil) btnLinkPerfil.style.display = 'none';
                } else if (sesionActiva.plan === 'Individual' || sesionActiva.plan === 'Estudiantes') {
                    tituloSec.textContent = "Usuario Vinculado:";
                    famCont.textContent = `${sesionActiva.nombre} (${sesionActiva.correo})`;
                    if (contenedorCupos) contenedorCupos.style.display = 'none';
                    if (btnLinkPerfil) btnLinkPerfil.style.display = 'none';
                } else {
                    tituloSec.textContent = "Miembros Vinculados (Titular + Invitados con contraseña):";
                    let titularObj = usuariosDB.find(u => u.correo.toLowerCase() === sesionActiva.correo.toLowerCase());
                    let listaMiembros = titularObj && titularObj.invitados ? titularObj.invitados : [{nombre: sesionActiva.nombre, correo: sesionActiva.correo}];
                    famCont.innerHTML = listaMiembros.map(f => `• ${f.nombre} (${f.correo})`).join('<br>');
                    
                    if (btnLinkPerfil) btnLinkPerfil.style.display = 'block';

                    if (contenedorCupos && (sesionActiva.plan === 'Dúo' || sesionActiva.plan === 'Familiar')) {
                        contenedorCupos.style.display = 'block';
                        let maxInv = sesionActiva.plan === 'Dúo' ? 1 : 5;
                        let invitadosActuales = Math.max(0, listaMiembros.length - 1);
                        txtCupos.textContent = `Cupos de Invitación usados: ${invitadosActuales} / ${maxInv} máx (Titular ocupa 1 lugar)`;
                    }
                }
            }
            actualizarSidebar();
        }

        function toggleMenuSeguridadPerfil() {
            const submenu = document.getElementById('contenedorSubmenuSeguridad');
            const flecha = document.getElementById('flechaSeguridad');
            if (submenu.style.display === 'none' || !submenu.style.display) {
                submenu.style.display = 'flex';
                flecha.textContent = '▲';
                document.getElementById('inputVerPassPerfil').value = sesionActiva ? sesionActiva.password : '';
            } else {
                submenu.style.display = 'none';
                flecha.textContent = '▼';
            }
        }

        function toggleVerPasswordPerfilActual(btn) {
            const input = document.getElementById('inputVerPassPerfil');
            if (input.type === 'password') {
                input.type = 'text';
                btn.textContent = '🙈';
            } else {
                input.type = 'password';
                btn.textContent = '👁️';
            }
        }

        function cambiarPasswordDesdePerfil() {
            const actual = document.getElementById('perfilPassActual').value.trim();
            const nueva1 = document.getElementById('perfilPassNueva1').value.trim();
            const nueva2 = document.getElementById('perfilPassNueva2').value.trim();

            if (!actual || !nueva1 || !nueva2) {
                mostrarToast("Rellena todos los campos de contraseña.");
                return;
            }
            if (actual !== sesionActiva.password) {
                mostrarToast("La contraseña actual es incorrecta.");
                return;
            }
            if (nueva1 !== nueva2) {
                mostrarToast("Las nuevas contraseñas no coinciden.");
                return;
            }

            sesionActiva.password = nueva1;
            let idx = usuariosDB.findIndex(u => u.correo.toLowerCase() === sesionActiva.correo.toLowerCase());
            if (idx >= 0) usuariosDB[idx] = sesionActiva;

            localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));

            document.getElementById('perfilPassActual').value = '';
            document.getElementById('perfilPassNueva1').value = '';
            document.getElementById('perfilPassNueva2').value = '';
            document.getElementById('inputVerPassPerfil').value = sesionActiva.password;

            mostrarToast("¡Contraseña actualizada con éxito desde el perfil!");
        }

        function iniciarCambioPaquete(nuevoPlan) {
            if (nuevoPlan === sesionActiva.plan) return;

            if (sesionActiva.plan === 'Estudiantes' && nuevoPlan !== 'Estudiantes') {
                cerrarModales();
                document.getElementById('tituloModalCorreoPersonalizado').textContent = "Cambio a Plan Comercial Requerido";
                document.getElementById('descModalCorreoPersonalizado').innerHTML = "Estás saliendo del <strong>Plan Estudiantes</strong>. Debes ingresar un correo personal válido (@gmail.com o @yahoo.com) para continuar con el nuevo paquete:";
                document.getElementById('labelInputCorreoModal').textContent = "Nuevo correo personal (Gmail o Yahoo):";
                document.getElementById('inputCorreoPersonalizadoNuevo').value = "";
                document.getElementById('modalCambioCorreoPersonalizado').style.display = 'flex';
                window._planPendienteCambio = nuevoPlan;
                return;
            }

            if (sesionActiva.plan !== 'Estudiantes' && nuevoPlan === 'Estudiantes') {
                cerrarModales();
                document.getElementById('tituloModalCorreoPersonalizado').textContent = "Correo Institucional Requerido";
                document.getElementById('descModalCorreoPersonalizado').innerHTML = "Para cambiar al <strong>Plan Estudiantes</strong> debes ingresar obligatoriamente tu correo institucional (@alumnos.utleon.edu.mx):";
                document.getElementById('labelInputCorreoModal').textContent = "Correo institucional universitario:";
                document.getElementById('inputCorreoPersonalizadoNuevo').value = "";
                document.getElementById('modalCambioCorreoPersonalizado').style.display = 'flex';
                window._planPendienteCambio = 'Estudiantes';
                return;
            }

            ejecutarFlujoCambioPlanDirecto(nuevoPlan, sesionActiva.correo);
        }

        function guardarCorreoPersonalizadoYContinuar() {
            const nuevoCorreo = document.getElementById('inputCorreoPersonalizadoNuevo').value.trim().toLowerCase();
            const planDestino = window._planPendienteCambio || 'Individual';

            if (!nuevoCorreo || !nuevoCorreo.includes("@")) {
                mostrarToast("⚠️ Debes ingresar un correo electrónico válido.");
                return;
            }

            if (planDestino === 'Estudiantes' && !nuevoCorreo.endsWith("@alumnos.utleon.edu.mx")) {
                mostrarToast("⚠️ El Plan Estudiantes requiere estrictamente un correo institucional (@alumnos.utleon.edu.mx).");
                return;
            }

            if (planDestino !== 'Estudiantes' && (nuevoCorreo.endsWith("@alumnos.utleon.edu.mx") || !validarDominioCorreo(nuevoCorreo))) {
                mostrarToast("⚠️ Para este plan comercial debes ingresar un correo personal válido (@gmail.com o @yahoo.com).");
                return;
            }

            sesionActiva.correo = nuevoCorreo;
            let idx = usuariosDB.findIndex(u => u.nombre.toLowerCase() === sesionActiva.nombre.toLowerCase());
            if (idx >= 0) usuariosDB[idx] = sesionActiva;
            localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
            localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));

            document.getElementById('modalCambioCorreoPersonalizado').style.display = 'none';
            mostrarToast("¡Correo actualizado con éxito!");
            
            let invitacionesLimpias = [{ nombre: sesionActiva.nombre, correo: sesionActiva.correo, password: sesionActiva.password }];
            prepararPagoCambioPlan(planDestino, invitacionesLimpias);
        }

        function ejecutarFlujoCambioPlanDirecto(nuevoPlan, correoUsar) {
            mostrarConfirmCustom(
                "Confirmación de Cambio",
                `¿Seguro que quieres cambiar de paquete a ${nuevoPlan}? Se requiere verificación de pago.`,
                (aceptado) => {
                    if (aceptado) {
                        cerrarModales();
                        let invitacionesLimpias = [{ nombre: sesionActiva.nombre, correo: correoUsar, password: sesionActiva.password }];
                        prepararPagoCambioPlan(nuevoPlan, invitacionesLimpias);
                    } else {
                        document.getElementById('selectCambiarPaquete').value = sesionActiva.plan;
                    }
                },
                "Sí, proceder al pago"
            );
        }

        function prepararPagoCambioPlan(plan, invitados) {
            temporalRegistroData = {
                nombre: sesionActiva.nombre,
                correo: sesionActiva.correo,
                password: sesionActiva.password,
                plan: plan,
                fechaRegistro: new Date().getTime(),
                invitados: invitados,
                esInvitado: false,
                titularAsociado: null,
                esCambioPlan: true
            };

            document.getElementById('authOverlay').style.display = 'flex';
            document.getElementById('cardRegistro').style.display = 'none';
            document.getElementById('cardLogin').style.display = 'none';
            document.getElementById('cardOlvido').style.display = 'none';
            document.getElementById('cardRegistroInvitada').style.display = 'none';
            document.getElementById('cardRegistroMiembroCambio').style.display = 'none';
            document.getElementById('cardPago').style.display = 'flex';
            
            document.getElementById('tituloPagoCard').textContent = `Verificación de Pago por Cambio a Plan ${plan}`;
            
            const inputCorreoVerif = document.getElementById('inputCorreoVerificacion');
            inputCorreoVerif.value = sesionActiva.correo;
            inputCorreoVerif.disabled = true;

            const btnAcceder = document.getElementById('btnAccederPlataforma');
            btnAcceder.disabled = true;
            btnAcceder.style.opacity = '0.4';
            btnAcceder.style.cursor = 'not-allowed';

            const infoP = infoPlanesData[plan] || infoPlanesData['Individual'];
            document.getElementById('resumenPlanNombre').textContent = `Nuevo Plan Seleccionado: ${plan}`;
            document.getElementById('resumenPlanDesc').textContent = infoP.desc;
            document.getElementById('resumenPlanPrecio').textContent = `Total a pagar: ${infoP.precio}`;
            document.getElementById('textoPagoDesc').textContent = `Haz clic para mandar el código de verificación de pago a ${sesionActiva.correo}.`;
            document.getElementById('inputCodigoIngresado').value = '';
        }

        let usuario = sesionActiva ? sesionActiva.nombre : "Usuario";
        
        // RECUPERACIÓN SEGURA DE PLAYLISTS Y FAVORITOS SEGÚN EL USUARIO ACTIVO
        let playlists = sesionActiva ? (JSON.parse(localStorage.getItem('sp_pls_' + sesionActiva.correo)) || []) : [];
        let favoritos = sesionActiva ? (JSON.parse(localStorage.getItem('sp_favs_' + sesionActiva.correo)) || []) : [];
        
        let historialBusqueda = JSON.parse(localStorage.getItem('sp_hist')) || ["santa fe klan", "luis miguel"];
        let colaReproduccion = [];
        let colaOriginal = [];
        let indiceActual = -1;
        let cancionSeleccionada = null;
        let playlistActualIndex = null;
        let playlistRenombrarIndex = null;
        let timeoutBusqueda = null;

        let isShuffleActive = false;
        let isRepeatActive = false;
        let duracionTotalSegundos = 210; 
        let tiempoActualSegundos = 0;
        let timerProgreso = null;
        let reproduciendo = false;
        let videoCargadoYReproduciendo = false;
        let videoActualId = null;

        const inputBuscador = document.getElementById('buscadorInput');
        const progressSlider = document.getElementById('progressSlider');
        const playPauseBtn = document.getElementById('playPauseBtn');

        window.addEventListener('message', function(event) {
            try {
                if (typeof event.data === 'string') {
                    const data = JSON.parse(event.data);
                    if (data.event === 'infoDelivery' && data.info) {
                        if (typeof data.info.currentTime === 'number') {
                            tiempoActualSegundos = Math.floor(data.info.currentTime);
                            actualizarUIProgreso(tiempoActualSegundos);
                        }
                        if (typeof data.info.duration === 'number' && data.info.duration > 0) {
                            duracionTotalSegundos = Math.floor(data.info.duration);
                            document.getElementById('totalTime').textContent = formatearTiempo(duracionTotalSegundos);
                            document.getElementById('npTotalTime').textContent = formatearTiempo(duracionTotalSegundos);
                        }
                        if (data.info.playerState === 1) {
                            videoCargadoYReproduciendo = true;
                            reproduciendo = true;
                            playPauseBtn.textContent = "⏸";
                            document.getElementById('npPlayBtn').textContent = "⏸";
                        } else if (data.info.playerState === 2) {
                            reproduciendo = false;
                            playPauseBtn.textContent = "▶";
                            document.getElementById('npPlayBtn').textContent = "▶";
                        } else if (data.info.playerState === 0) {
                            if (isRepeatActive) reproducirPorIndice(indiceActual);
                            else reproducirSiguiente();
                        }
                    }
                }
            } catch(e) {}
        });

        function actualizarUIProgreso(segundos) {
            const fmt = formatearTiempo(segundos);
            document.getElementById('currentTime').textContent = fmt;
            document.getElementById('npCurrentTime').textContent = fmt;
            if (duracionTotalSegundos > 0) {
                const pct = (segundos / duracionTotalSegundos) * 100;
                progressSlider.value = pct;
                document.getElementById('npProgressSlider').value = pct;
            }
        }

        function solicitarTiempoYouTube() {
            const iframe = document.getElementById('ytPlayerEmbed');
            if (iframe && iframe.contentWindow) {
                iframe.contentWindow.postMessage(JSON.stringify({"event": "command", "func": "getCurrentTime", "args": []}), '*');
                iframe.contentWindow.postMessage(JSON.stringify({"event": "listening", "id": 1}), '*');
            }
        }

        function moverIframeA(modo) {
            const iframe = document.getElementById('ytPlayerEmbed');
            const miniTarget = document.getElementById('miniVideoTarget');
            const bigTarget = document.getElementById('bigVideoTarget');
            const miniCont = document.getElementById('ytMiniPlayerContainer');
            const bigBox = document.getElementById('bigVideoBox');
            const coverImg = document.getElementById('npCoverImg');

            if (modo === 'big') {
                bigTarget.appendChild(iframe);
                bigBox.style.display = 'block';
                coverImg.style.display = 'none';
                miniCont.style.display = 'none';
            } else if (modo === 'mini') {
                miniTarget.appendChild(iframe);
                miniCont.style.display = 'block';
                bigBox.style.display = 'none';
                coverImg.style.display = 'block';
            }
        }

        function convertirTextoASegundos(texto) {
            if (!texto) return 210;
            const partes = texto.split(':').map(Number);
            if (partes.length === 3) return partes[0] * 3600 + partes[1] * 60 + partes[2];
            else if (partes.length === 2) return partes[0] * 60 + partes[1];
            return 210;
        }

        function abrirNowPlaying() {
            if (indiceActual >= 0) {
                document.getElementById('nowPlayingOverlay').style.display = 'flex';
                actualizarBotonCheck();
            }
        }
        function cerrarNowPlaying() { document.getElementById('nowPlayingOverlay').style.display = 'none'; }

        function accionBotonVerVideo() {
            const bigBox = document.getElementById('bigVideoBox');
            const miniCont = document.getElementById('ytMiniPlayerContainer');
            if (bigBox.style.display === 'block') minimizarVideoAGrande();
            else if (miniCont.style.display === 'block') cerrarVideoCompleto();
            else moverIframeA('big');
        }

        function agrandarVideoAPortada() { moverIframeA('big'); }
        function minimizarVideoAGrande() { moverIframeA('mini'); }
        function cerrarVideoCompleto() {
            document.getElementById('ytMiniPlayerContainer').style.display = 'none';
            document.getElementById('bigVideoBox').style.display = 'none';
            document.getElementById('npCoverImg').style.display = 'block';
        }

        function abrirQueueOverlay() {
            document.getElementById('queueOverlay').style.display = 'flex';
            renderQueueItems();
        }
        function cerrarQueueOverlay() { document.getElementById('queueOverlay').style.display = 'none'; }

        let draggedIndex = null;
        function renderQueueItems() {
            const container = document.getElementById('queueContainer');
            container.innerHTML = '';
            colaReproduccion.forEach((item, index) => {
                const isPlaying = index === indiceActual;
                const div = document.createElement('div');
                div.className = 'queue-item';
                div.draggable = true;
                div.innerHTML = `
                    <div class="queue-item-left" onclick="reproducirPorIndice(${index})">
                        <img src="${item.imagen}">
                        <div class="queue-item-info">
                            <div class="queue-item-name" style="color: ${isPlaying ? '#1db954' : '#fff'};">${item.titulo}</div>
                            <div class="queue-item-artist">${item.artista}</div>
                        </div>
                    </div>
                    <div class="queue-drag-handle">≡</div>
                `;
                div.addEventListener('dragstart', () => { draggedIndex = index; div.classList.add('dragging'); });
                div.addEventListener('dragend', () => { div.classList.remove('dragging'); });
                div.addEventListener('dragover', (e) => { e.preventDefault(); });
                div.addEventListener('drop', (e) => {
                    e.preventDefault();
                    if (draggedIndex !== null && draggedIndex !== index) {
                        const movedItem = colaReproduccion.splice(draggedIndex, 1)[0];
                        colaReproduccion.splice(index, 0, movedItem);
                        if (indiceActual === draggedIndex) indiceActual = index;
                        else if (draggedIndex < indiceActual && index >= indiceActual) indiceActual--;
                        else if (draggedIndex > indiceActual && index <= indiceActual) indiceActual++;
                        renderQueueItems();
                    }
                });
                container.appendChild(div);
            });
        }

        function mostrarDropdown() {
            document.getElementById('searchDropdown').style.display = 'block';
            actualizarHistorialUI();
        }

        function cerrarMenusGlobal(e) {
            if (!e.target.closest('.context-menu') && !e.target.closest('.btn-dots')) {
                document.getElementById('contextMenu').style.display = 'none';
                document.getElementById('subMenuPlaylists').style.display = 'none';
            }
            if (!e.target.closest('.search-container')) {
                document.getElementById('searchDropdown').style.display = 'none';
            }
        }

        function actualizarHistorialUI() {
            const contenedor = document.getElementById('listaHistorial');
            contenedor.innerHTML = '';
            historialBusqueda.slice(-5).reverse().forEach(term => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.innerHTML = `
                    <span onclick="ejecutarBusquedaHistorial('${term}')">🕒 ${term}</span>
                    <button class="history-delete" onclick="event.stopPropagation(); borrarHistorial('${term}')">✕</button>
                `;
                contenedor.appendChild(div);
            });
        }

        function borrarHistorial(term) {
            historialBusqueda = historialBusqueda.filter(h => h !== term);
            localStorage.setItem('sp_hist', JSON.stringify(historialBusqueda));
            actualizarHistorialUI();
        }

        function ejecutarBusquedaHistorial(term) {
            inputBuscador.value = term;
            document.getElementById('searchDropdown').style.display = 'none';
            buscarMusica(term);
        }

        function limpiarBusqueda() {
            inputBuscador.value = '';
            document.getElementById('searchClear').style.display = 'none';
            const grid = document.getElementById('gridResultados');
            if (grid) grid.innerHTML = '';
            const msg = document.getElementById('mensajeEstado');
            if (msg) msg.textContent = "Busca cualquier artista, canción, álbum o podcast...";
        }

        function manejarBusquedaInput(e) {
            const query = e.target.value.trim();
            const clearBtn = document.getElementById('searchClear');
            clearBtn.style.display = query ? 'block' : 'none';

            clearTimeout(timeoutBusqueda);
            if (!query || query.length < 3) return;

            timeoutBusqueda = setTimeout(() => {
                if (!historialBusqueda.includes(query)) {
                    historialBusqueda.push(query);
                    localStorage.setItem('sp_hist', JSON.stringify(historialBusqueda));
                }
                buscarMusica(query);
            }, 500);
        }

        function buscarDirecto(termino) {
            inputBuscador.value = termino;
            document.getElementById('searchClear').style.display = 'block';
            buscarMusica(termino);
        }

        async function buscarMusica(query) {
            if (!query) return;
            if (!document.getElementById('gridResultados')) {
                irAInicio();
                inputBuscador.value = query;
            }

            document.getElementById('searchDropdown').style.display = 'none';
            document.getElementById('mensajeEstado').textContent = "Buscando canciones de \"" + query + "\" ...";
            const grid = document.getElementById('gridResultados');
            grid.innerHTML = '';

            try {
                const resp = await fetch("/api/spotify/" + encodeURIComponent(query));
                const data = await resp.json();

                if (data.error || !data.resultados || data.resultados.length === 0) {
                    document.getElementById('mensajeEstado').textContent = "No se encontraron resultados para \"" + query + "\".";
                    return;
                }

                colaOriginal = data.resultados;
                colaReproduccion = [...colaOriginal];
                
                playlistActualIndex = null;
                document.getElementById('npHeaderCategory').textContent = "REPRODUCIENDO DESDE BÚSQUEDA";
                document.getElementById('npPlaylistTitle').textContent = query;
                document.getElementById('queueSubtitle').textContent = "Resultados para: " + query;

                document.getElementById('mensajeEstado').textContent = "Se encontraron " + colaReproduccion.length + " canciones para \"" + query + "\":";

                colaReproduccion.forEach((item, index) => {
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `
                        <img src="${item.imagen}" alt="${item.titulo}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="overflow:hidden;">
                                <div class="card-title">${item.titulo}</div>
                                <div class="card-subtitle">${item.artista} • ${item.duracionTexto || "3:30"}</div>
                            </div>
                            <button class="btn-dots" onclick="abrirMenuContextual(event, ${index}, null)">⋮</button>
                        </div>
                    `;
                    card.onclick = () => reproducirPorIndice(index);
                    grid.appendChild(card);
                });
            } catch(e) {
                document.getElementById('mensajeEstado').textContent = "Error de conexión con el servidor.";
            }
        }

        function esMismaCancion(c1, c2) {
            if (!c1 || !c2) return false;
            if (c1.videoId && c2.videoId) return c1.videoId === c2.videoId;
            return c1.titulo === c2.titulo;
        }

        function reproducirPorIndice(index) {
            if (index >= 0 && index < colaReproduccion.length) {
                indiceActual = index;
                const item = colaReproduccion[indiceActual];

                duracionTotalSegundos = convertirTextoASegundos(item.duracionTexto);
                videoCargadoYReproduciendo = false;
                tiempoActualSegundos = 0;
                actualizarUIProgreso(0);

                document.getElementById('playerTitle').textContent = item.titulo;
                document.getElementById('playerArtist').textContent = item.artista;
                document.getElementById('playerImg').src = item.imagen;

                document.getElementById('npTitle').textContent = item.titulo;
                document.getElementById('npArtist').textContent = item.artista;
                document.getElementById('npCoverImg').src = item.imagen;
                
                actualizarBotonCheck();

                if (item.videoId) {
                    const iframe = document.getElementById('ytPlayerEmbed');
                    if (videoActualId !== item.videoId) {
                        videoActualId = item.videoId;
                        iframe.src = "https://www.youtube.com/embed/" + item.videoId + "?autoplay=1&enablejsapi=1&widgetid=1";
                    } else {
                        iframe.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
                    }
                    playPauseBtn.textContent = "⏸";
                    document.getElementById('npPlayBtn').textContent = "⏸";
                    iniciarRelojProgreso();
                }

                if (document.getElementById('queueOverlay').style.display === 'flex') {
                    renderQueueItems();
                }
            }
        }

        function actualizarBotonCheck() {
            if (indiceActual < 0 || indiceActual >= colaReproduccion.length) return;
            const item = colaReproduccion[indiceActual];
            const checkBtn = document.getElementById('npCheckBtn');
            const favBtn = document.getElementById('playerFavBtn');

            let estaGuardada = false;
            if (playlistActualIndex !== null && playlistActualIndex !== undefined) {
                const pl = playlists[playlistActualIndex];
                if (pl && pl.canciones) estaGuardada = pl.canciones.some(c => esMismaCancion(c, item));
            } else {
                estaGuardada = favoritos.some(f => esMismaCancion(f, item));
            }

            if (estaGuardada) {
                checkBtn.classList.remove('desmarcado');
                checkBtn.textContent = '✓';
                if (favBtn) favBtn.classList.add('active');
            } else {
                checkBtn.classList.add('desmarcado');
                checkBtn.textContent = '+';
                if (favBtn) favBtn.classList.remove('active');
            }
        }

        function toggleFavoritoActual() {
            if (indiceActual < 0 || indiceActual >= colaReproduccion.length) return;
            const item = colaReproduccion[indiceActual];

            if (playlistActualIndex !== null && playlistActualIndex !== undefined) {
                const pl = playlists[playlistActualIndex];
                const idx = pl.canciones.findIndex(c => esMismaCancion(c, item));
                if (idx >= 0) {
                    pl.canciones.splice(idx, 1);
                    mostrarToast("Eliminado de " + pl.nombre);
                } else {
                    pl.canciones.push(item);
                    mostrarToast("Añadido a " + pl.nombre);
                }
                if (sesionActiva) localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
                if (document.getElementById('contenidoDinamico').querySelector('.playlist-header')) {
                    abrirDetallePlaylist(playlistActualIndex);
                }
            } else {
                const idx = favoritos.findIndex(f => esMismaCancion(f, item));
                if (idx >= 0) {
                    favoritos.splice(idx, 1);
                    mostrarToast("Eliminado de Tus Me Gusta");
                } else {
                    favoritos.push(item);
                    mostrarToast("Añadido a Tus Me Gusta ❤️");
                }
                if (sesionActiva) localStorage.setItem('sp_favs_' + sesionActiva.correo, JSON.stringify(favoritos));
                if (document.getElementById('contenidoDinamico').querySelector('.playlist-header')) {
                    verFavoritos();
                }
            }
            actualizarBotonCheck();
        }

        function iniciarRelojProgreso() {
            clearInterval(timerProgreso);
            reproduciendo = true;
            document.getElementById('totalTime').textContent = formatearTiempo(duracionTotalSegundos);
            document.getElementById('npTotalTime').textContent = formatearTiempo(duracionTotalSegundos);
            timerProgreso = setInterval(() => { solicitarTiempoYouTube(); }, 300);
        }

        function cambiarProgreso(val) {
            tiempoActualSegundos = Math.floor((val / 100) * duracionTotalSegundos);
            actualizarUIProgreso(tiempoActualSegundos);
            const iframe = document.getElementById('ytPlayerEmbed');
            if (iframe && iframe.contentWindow) {
                iframe.contentWindow.postMessage(JSON.stringify({"event": "command", "func": "seekTo", "args": [tiempoActualSegundos, true]}), '*');
            }
        }

        function formatearTiempo(sec) {
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return m + ":" + (s < 10 ? "0" : "") + s;
        }

        function toggleShuffle() {
            isShuffleActive = !isShuffleActive;
            const btn = document.getElementById('btnShuffle');
            const btnNP = document.getElementById('btnShuffleNP');
            if (isShuffleActive) {
                btn.classList.add('active-blue');
                btnNP.classList.add('active-blue');
                if (colaReproduccion.length > 1) {
                    let actual = colaReproduccion[indiceActual];
                    colaReproduccion.sort(() => Math.random() - 0.5);
                    if (actual) indiceActual = colaReproduccion.findIndex(c => esMismaCancion(c, actual));
                }
                mostrarToast("Modo Aleatorio ACTIVADO 🔀");
            } else {
                btn.classList.remove('active-blue');
                btnNP.classList.remove('active-blue');
                colaReproduccion = [...colaOriginal];
                mostrarToast("Modo Aleatorio DESACTIVADO");
            }
        }

        function toggleRepeat() {
            isRepeatActive = !isRepeatActive;
            const btn = document.getElementById('btnRepeat');
            const btnNP = document.getElementById('btnRepeatNP');
            if (isRepeatActive) {
                btn.classList.add('active-blue');
                btnNP.classList.add('active-blue');
                mostrarToast("Repetir canción ACTIVADO 🔁");
            } else {
                btn.classList.remove('active-blue');
                btnNP.classList.remove('active-blue');
                mostrarToast("Repetir canción DESACTIVADO");
            }
        }

        function reproducirSiguiente() {
            if (colaReproduccion.length > 0) {
                let nuevoIndice = (indiceActual + 1) % colaReproduccion.length;
                reproducirPorIndice(nuevoIndice);
            }
        }

        function reproducirAnterior() {
            if (colaReproduccion.length > 0) {
                let nuevoIndice = (indiceActual - 1 + colaReproduccion.length) % colaReproduccion.length;
                reproducirPorIndice(nuevoIndice);
            }
        }

        function togglePlay() {
            const iframe = document.getElementById('ytPlayerEmbed');
            if (!iframe || !iframe.contentWindow) return;
            reproduciendo = !reproduciendo;
            if (reproduciendo) {
                iframe.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
                playPauseBtn.textContent = "⏸";
                document.getElementById('npPlayBtn').textContent = "⏸";
            } else {
                iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
                playPauseBtn.textContent = "▶";
                document.getElementById('npPlayBtn').textContent = "▶";
            }
        }

        function abrirMenuContextualActual(e) {
            if (indiceActual >= 0) abrirMenuContextual(e, indiceActual, null);
        }

        function abrirMenuContextual(e, index, plIndex) {
            e.stopPropagation();
            cancionSeleccionada = colaReproduccion[index];
            playlistActualIndex = plIndex;
            const menu = document.getElementById('contextMenu');
            menu.style.display = 'block';
            menu.style.left = Math.min(e.clientX, window.innerWidth - 240) + 'px';
            menu.style.top = Math.min(e.clientY, window.innerHeight - 200) + 'px';
            document.getElementById('subMenuPlaylists').style.display = 'none';
        }

        function reproducirDespues() {
            if (indiceActual >= 0) {
                colaReproduccion.splice(indiceActual + 1, 0, cancionSeleccionada);
            } else {
                colaReproduccion.push(cancionSeleccionada);
                reproducirPorIndice(colaReproduccion.length - 1);
            }
            mostrarToast("Añadido a la fila de reproducción.");
            document.getElementById('contextMenu').style.display = 'none';
        }

        function abrirSubMenuPlaylists(e) {
            e.stopPropagation();
            const sub = document.getElementById('subMenuPlaylists');
            const main = document.getElementById('contextMenu');
            sub.style.display = 'block';
            sub.style.left = (parseInt(main.style.left) - 210) + 'px';
            sub.style.top = main.style.top;
            
            const contenedor = document.getElementById('listaOpcionesPlaylists');
            contenedor.innerHTML = '';
            playlists.forEach((pl, idx) => {
                const div = document.createElement('div');
                div.className = 'context-item';
                div.textContent = pl.nombre;
                div.onclick = (event) => {
                    event.stopPropagation();
                    pl.canciones.push(cancionSeleccionada);
                    if (sesionActiva) localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
                    mostrarToast("Añadido a " + pl.nombre);
                    sub.style.display = 'none';
                    main.style.display = 'none';
                };
                contenedor.appendChild(div);
            });
        }

        function agregarFavoritosDirecto() {
            if (!favoritos.some(f => esMismaCancion(f, cancionSeleccionada))) {
                favoritos.push(cancionSeleccionada);
                if (sesionActiva) localStorage.setItem('sp_favs_' + sesionActiva.correo, JSON.stringify(favoritos));
                mostrarToast("Añadido a Tus Me Gusta ❤️");
            } else {
                mostrarToast("Esta canción ya está en tus favoritos.");
            }
            document.getElementById('contextMenu').style.display = 'none';
        }

        function eliminarCancionActualContexto() {
            if (playlistActualIndex !== null && playlistActualIndex !== undefined) {
                playlists[playlistActualIndex].canciones = playlists[playlistActualIndex].canciones.filter(c => !esMismaCancion(c, cancionSeleccionada));
                if (sesionActiva) localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
                abrirDetallePlaylist(playlistActualIndex);
            } else {
                favoritos = favoritos.filter(f => !esMismaCancion(f, cancionSeleccionada));
                if (sesionActiva) localStorage.setItem('sp_favs_' + sesionActiva.correo, JSON.stringify(favoritos));
                verFavoritos();
            }
            mostrarToast("Eliminado.");
            document.getElementById('contextMenu').style.display = 'none';
        }

        function irAInicio() {
            playlistActualIndex = null;
            document.getElementById('contenidoDinamico').innerHTML = `
                <div class="filter-chips">
                    <button class="filter-chip active" onclick="filtrarTab('todo', this)">Todo</button>
                    <button class="filter-chip" onclick="filtrarTab('musica', this)">Música</button>
                    <button class="filter-chip" onclick="filtrarTab('podcasts', this)">Podcasts 🎙️</button>
                </div>
                <div id="vistaDinamica">
                    <section>
                        <h2 class="section-title" style="font-size: 1.3rem; margin-bottom: 12px;">Catálogo Mundial Infinito</h2>
                        <div class="cards-grid">
                            <div class="card" onclick="buscarDirecto('Santa Fe Klan')">
                                <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&auto=format&fit=crop&q=80" alt="Santa Fe Klan">
                                <div class="card-title">Santa Fe Klan</div>
                                <div class="card-subtitle">Todo el repertorio</div>
                            </div>
                            <div class="card" onclick="buscarDirecto('Luis Miguel')">
                                <img src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&auto=format&fit=crop&q=80" alt="Luis Miguel">
                                <div class="card-title">Luis Miguel</div>
                                <div class="card-subtitle">Discografía completa</div>
                            </div>
                            <div class="card" onclick="buscarDirecto('Podcast Exitosos')">
                                <img src="https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=300&auto=format&fit=crop&q=80" alt="Podcasts">
                                <div class="card-title">Podcasts Globales</div>
                                <div class="card-subtitle">Todos los programas y episodios</div>
                            </div>
                        </div>
                    </section>
                    <section style="margin-top: 25px;">
                        <h2 class="section-title" id="tituloResultados" style="font-size: 1.3rem; margin-bottom: 12px;">Resultados</h2>
                        <div id="mensajeEstado" style="color: #a7a7a7; font-size: 0.9rem; margin-bottom: 10px;">Busca cualquier artista, canción, álbum o podcast...</div>
                        <div id="gridResultados" class="cards-grid"></div>
                    </section>
                </div>
            `;
        }

        function verFavoritos() {
            playlistActualIndex = null;
            document.getElementById('npHeaderCategory').textContent = "REPRODUCIENDO DESDE FAVORITOS";
            document.getElementById('npPlaylistTitle').textContent = "Tus Me Gusta";
            document.getElementById('queueSubtitle').textContent = "Reproduciendo Tus Me Gusta";
            const cont = document.getElementById('contenidoDinamico');
            cont.innerHTML = `
                <div class="playlist-header" style="background: linear-gradient(to bottom, #50388c, #121212);">
                    <img src="https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=300" alt="Fav">
                    <div class="playlist-header-meta">
                        <span style="font-size:0.85rem; font-weight:bold;">Playlist oficial</span>
                        <h1>Tus Me Gusta</h1>
                        <p style="color:#b3b3b3; margin-top:5px;">${favoritos.length} elementos guardados</p>
                    </div>
                </div>
                <table class="songs-table">
                    <tr><th>#</th><th>Título</th><th>Artista</th><th>Duración</th><th>Acción</th></tr>
                    ${favoritos.map((c, i) => `
                        <tr onclick='reproducirPorIndice(${i})'>
                            <td>${i+1}</td>
                            <td><div class="song-title-cell"><img src="${c.imagen}"> ${c.titulo}</div></td>
                            <td>${c.artista}</td>
                            <td>${c.duracionTexto || "3:30"}</td>
                            <td><button class="btn-dots" onclick="abrirMenuContextual(event, ${i}, null)">⋮</button></td>
                        </tr>
                    `).join('')}
                </table>
            `;
            colaOriginal = favoritos;
            colaReproduccion = favoritos;
        }

        function abrirDetallePlaylist(idx) {
            const pl = playlists[idx];
            playlistActualIndex = idx;
            document.getElementById('npHeaderCategory').textContent = "REPRODUCIENDO DESDE PLAYLIST";
            document.getElementById('npPlaylistTitle').textContent = pl.nombre;
            document.getElementById('queueSubtitle').textContent = "Reproduciendo " + pl.nombre;
            const cont = document.getElementById('contenidoDinamico');
            cont.innerHTML = `
                <div class="playlist-header">
                    <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300" alt="PL">
                    <div class="playlist-header-meta">
                        <span style="font-size:0.85rem; font-weight:bold;">Playlist pública</span>
                        <h1>${pl.nombre}</h1>
                        <p style="color:#b3b3b3; margin-top:5px;">${usuario} • ${pl.canciones.length} elementos</p>
                    </div>
                </div>
                <table class="songs-table">
                    <tr><th>#</th><th>Título</th><th>Artista</th><th>Duración</th><th>Acción</th></tr>
                    ${pl.canciones.map((c, i) => `
                        <tr onclick='reproducirPorIndice(${i})'>
                            <td>${i+1}</td>
                            <td><div class="song-title-cell"><img src="${c.imagen}"> ${c.titulo}</div></td>
                            <td>${c.artista}</td>
                            <td>${c.duracionTexto || "3:30"}</td>
                            <td><button class="btn-dots" onclick="abrirMenuContextual(event, ${i}, ${idx})">⋮</button></td>
                        </tr>
                    `).join('')}
                </table>
            `;
            colaOriginal = pl.canciones;
            colaReproduccion = pl.canciones;
        }

        function actualizarSidebar() {
            if (sesionActiva) {
                playlists = JSON.parse(localStorage.getItem('sp_pls_' + sesionActiva.correo)) || [];
            }
            const lista = document.getElementById('listaSidebar');
            lista.innerHTML = '';
            playlists.forEach((pl, i) => {
                const div = document.createElement('div');
                div.className = 'playlist-item';
                div.innerHTML = `
                    <div class="playlist-info" onclick="abrirDetallePlaylist(${i})">
                        <span class="playlist-name">${pl.nombre}</span>
                        <span class="playlist-owner">Playlist • ${usuario}</span>
                    </div>
                    <div class="playlist-actions-btn">
                        <button class="btn-action-pl" title="Renombrar" onclick="event.stopPropagation(); abrirModalRenombrar(${i})">✏️</button>
                        <button class="btn-action-pl" title="Eliminar" onclick="event.stopPropagation(); eliminarPlaylist(${i})">🗑️</button>
                    </div>
                `;
                lista.appendChild(div);
            });
        }

        function abrirModalRenombrar(idx) {
            playlistRenombrarIndex = idx;
            document.getElementById('inputRenombrarPl').value = playlists[idx].nombre;
            document.getElementById('modalRenombrar').style.display = 'flex';
        }

        function guardarRenombrarPlaylist() {
            const nuevo = document.getElementById('inputRenombrarPl').value.trim();
            if (nuevo && playlistRenombrarIndex !== null) {
                playlists[playlistRenombrarIndex].nombre = nuevo;
                if (sesionActiva) {
                    localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
                }
                actualizarSidebar();
                cerrarModales();
                mostrarToast("Playlist renombrada con éxito");
            }
        }

        function eliminarPlaylist(idx) {
            playlists.splice(idx, 1);
            if (sesionActiva) {
                localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
            }
            actualizarSidebar();
            mostrarToast("Playlist eliminada");
        }

        function abrirModalPlaylist() { 
            document.getElementById('inputNombrePl').value = '';
            document.getElementById('modalPlaylist').style.display = 'flex'; 
        }

        function abrirModalPerfil() {
            if (sesionActiva) {
                document.getElementById('inputNombrePerfil').value = sesionActiva.nombre;
                document.getElementById('selectCambiarPaquete').value = sesionActiva.plan || "Individual";
            }
            document.getElementById('modalPerfil').style.display = 'flex';
        }

        function cerrarModales() {
            document.getElementById('modalPlaylist').style.display = 'none';
            document.getElementById('modalRenombrar').style.display = 'none';
            document.getElementById('modalPerfil').style.display = 'none';
            document.getElementById('modalCambioCorreoPersonalizado').style.display = 'none';
        }

        function crearPlaylist() {
            const nombre = document.getElementById('inputNombrePl').value.trim();
            if (nombre) {
                playlists.push({ nombre, canciones: [] });
                if (sesionActiva) {
                    localStorage.setItem('sp_pls_' + sesionActiva.correo, JSON.stringify(playlists));
                }
                actualizarSidebar();
                cerrarModales();
                mostrarToast("Playlist creada con éxito");
            }
        }

        function guardarPerfil() {
            const nuevo = document.getElementById('inputNombrePerfil').value.trim();
            if (nuevo && sesionActiva) {
                sesionActiva.nombre = nuevo;
                usuario = nuevo;
                localStorage.setItem('sp_sesion_activa', JSON.stringify(sesionActiva));
                
                let idx = usuariosDB.findIndex(u => u.correo.toLowerCase() === sesionActiva.correo.toLowerCase());
                if (idx >= 0) {
                    usuariosDB[idx].nombre = nuevo;
                    localStorage.setItem('sp_usuarios_db', JSON.stringify(usuariosDB));
                }

                document.getElementById('nombreUsuarioLabel').textContent = usuario;
                document.getElementById('avatarLetra').textContent = usuario.charAt(0).toUpperCase();
                document.getElementById('perfilNombreLbl').textContent = usuario;
                cerrarModales();
                actualizarSidebar();
                mostrarToast("Perfil actualizado");
            }
        }

        function verPlaylistsGuardadas() { actualizarSidebar(); }
        function filtrarTab(t, btn) {
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const textoBuscador = document.getElementById('buscadorInput').value.trim();
            if (textoBuscador) buscarDirecto(textoBuscador);
            else {
                if(t==='podcasts') buscarDirecto('Podcast');
                if(t==='musica') buscarDirecto('Top Exitos');
                if(t==='todo') irAInicio();
            }
        }
    </script>
</body>
</html>
"""

class SpotifyInfinityServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/enviar-codigo":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            datos = json.loads(post_data.decode('utf-8'))
            correo_destino = datos.get("correo")

            import random
            codigo_seis = str(random.randint(100000, 999999))
            self.enviar_json({"success": True, "codigo": codigo_seis})
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/":
            contenido = PAGINA_WEB.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(contenido)))
            self.end_headers()
            self.wfile.write(contenido)
        elif parsed_url.path.startswith("/api/spotify/"):
            query = unquote(parsed_url.path[len("/api/spotify/"):]).strip()
            resultados = []
            query_musica = query + " cancion cancion oficial" if "cancion" not in query.lower() else query

            try:
                post_data = json.dumps({
                    "context": {
                        "client": {
                            "clientName": "WEB",
                            "clientVersion": "2.20240101.00.00",
                            "hl": "es",
                            "gl": "MX"
                        }
                    },
                    "query": query_musica
                }).encode("utf-8")
                
                req = urllib.request.Request(
                    "https://www.youtube.com/youtubei/v1/search",
                    data=post_data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=6) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    sections = res_json.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                    unique_ids = set()
                    
                    for section in sections:
                        items = section.get("itemSectionRenderer", {}).get("contents", [])
                        for item in items:
                            v_data = item.get("videoRenderer")
                            if v_data:
                                v_id = v_data.get("videoId")
                                title_runs = v_data.get("title", {}).get("runs", [])
                                title = title_runs[0].get("text") if title_runs else None
                                owner_runs = v_data.get("ownerText", {}).get("runs", [])
                                author = owner_runs[0].get("text") if owner_runs else "Artista"
                                length_text = v_data.get("lengthText", {}).get("simpleText", "3:30")
                                
                                if v_id and title and v_id not in unique_ids:
                                    unique_ids.add(v_id)
                                    resultados.append({
                                        "titulo": title,
                                        "artista": author,
                                        "imagen": f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg",
                                        "videoId": v_id,
                                        "duracionTexto": length_text
                                    })
                                    if len(resultados) >= 25:
                                        break
            except Exception as e:
                pass

            self.enviar_json({"resultados": resultados})
        else:
            self.enviar_json({"error": "Ruta no encontrada"})

    def enviar_json(self, data):
        contenido = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

import os

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8095))
    servidor = HTTPServer(("0.0.0.0", puerto), SpotifyInfinityServer)
    print(f"Servidor Spotify Master Edition iniciado en puerto {puerto}.")
    servidor.serve_forever()
