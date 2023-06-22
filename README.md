# Waveform Audio Player

**A web-based audio player with waveform visualisations.**

<img src="splash.png">

Provides a similar audio interface to [wavesurfer.js](https://wavesurfer-js.org/) or [SoundCloud](https://soundcloud.com/).

## Examples

Playback:

<img src="v2/preview.gif">

Customisation:

<img src="v2/settings.gif">

## Requirements

- Python 3.11+
- FFmpeg on PATH

## Version Differences

| Version 1 | Version 2 |
| --- | --- |
| Waveform is a pre-rendered image. | Waveform is rendered using HTML5 canvas. |
| Waveform size is fixed. | Waveform size is not fixed. |
| Output is a site containing the players. (Static site generator) | Output is a component that can be added to any site. |
| Basic playback animations. | Better playback animations with colour. |
| Playlist is just multiple players in a list. | Playlist uses one player and switches tracks. |
| No AJAX, can be opened locally. | AJAX, web server needed. |

### V1 Output

<img src="v1/v1.png">

### V2 Output

<img src="v2/v2.png">

## Usage

### Version 1

1. Put inputs as `.mp3` in the `inputs` folder.
2. Run `gen.py`.
3. View output in the `output` folder.

### Version 2

1. Put inputs as `.mp3` in the `inputs` folder.
2. Run `gen.py`.
3. Host the files on a web server.
4. Navigate to `index.html` in a web browser.

## Known Issues
- Seeking does not work for large files on Chrome, but does work on Firefox.
    - This is due to differences in how Chrome and Firefox handle streaming media.
    - To fix this, you must set `Accept-Ranges: bytes` in the HTTP response header for the audio files.
    - See [this.](https://stackoverflow.com/a/63059735)
