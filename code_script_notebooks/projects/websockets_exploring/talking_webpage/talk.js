talkify.config.remoteService.host = 'https://talkify.net';
talkify.config.remoteService.apiKey = '46b32f4e-6b73-40ee-8ae1-4a17cb1b18f6';
// The service requires API key as shown above

talkify.config.ui.audioControls.enabled = true; //<-- Disable to get the browser built in audio controls
talkify.config.ui.audioControls.voicepicker.enabled = true;
talkify.config.ui.audioControls.container = document.getElementById("player-and-voices");
  
$(document).ready(function() {
  var player = new talkify.TtsPlayer()
    .enableTextHighlighting()
    .forceVoice({name: "Zira"});

  var playlist = new talkify.playlist()
    .begin()
    .usingPlayer(player)
    .withRootSelector('#root')
    .withTextInteraction()
    .build();
  
  playlist.play();
});