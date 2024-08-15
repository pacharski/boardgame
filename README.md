Use board_editor to define spaces and paths (exits) to overlay on the board png image
The board is defined by a json file of 'spaces'
board_view is defined by an image file for the board with the spaces overlayed

When the board_editor is started, if there is a saved board json file it will be loaded

Use ctrl-M to change modes (rotate through the 3 modes)
  board editor has 3 modes, readonly (viewing), edit_spaces and edit_exits
readonly is just for looking at the board, zooming (double finger drag), scrolling around with mouse drags
edit_spaces: 
  mark the center of a space with the first mouse click
  mark vertices of the space outline with subsequent mouse clicks
  use ctrl-z to undo the last vertex, or center, or escape to abandone the space
  when all vertices are defined, optionally type level,name for the space
  then press enter to save the space

  ctrl-s will save the board data as a json file

To run tests for board_game model, from the board_game directory:
python model/test