let print_cells cells =
  List.iter (fun (x, y) -> Printf.printf "(%d, %d) " x y) cells;
  Printf.printf "\n"
;;

let print_l_shapes l_shapes =
  for i = 0 to List.length l_shapes - 1 do
    Printf.printf "Shape %d: " i;
    print_cells (List.nth l_shapes i)
  done
;;

let print_matrix matrix =
  Printf.printf "---------\n";
  Array.iter
    (fun row ->
      Array.iter (fun elem -> Printf.printf "%d " elem) row;
      Printf.printf "\n")
    matrix;
  Printf.printf "---------\n"
;;

let output_to_file matrix =
  let oc = open_out "output.txt" in
  Printf.fprintf oc "---------\n";
  Array.iter
    (fun row ->
      Array.iter (fun elem -> Printf.fprintf oc "%d " elem) row;
      Printf.fprintf oc "\n")
    matrix;
  Printf.fprintf oc "---------\n";
  close_out oc
;;

let clues_table_9 =
  let table = Hashtbl.create 14 in
  Hashtbl.add table (0, 1) 18;
  Hashtbl.add table (0, 6) 7;
  Hashtbl.add table (1, 4) 12;
  Hashtbl.add table (2, 2) 9;
  Hashtbl.add table (2, 7) 31;
  Hashtbl.add table (4, 1) 5;
  Hashtbl.add table (4, 3) 11;
  Hashtbl.add table (4, 5) 22;
  Hashtbl.add table (4, 7) 22;
  Hashtbl.add table (6, 1) 9;
  Hashtbl.add table (6, 6) 19;
  Hashtbl.add table (7, 4) 14;
  Hashtbl.add table (8, 2) 22;
  Hashtbl.add table (8, 7) 15;
  table
;;

let clues_table_5 =
  let table = Hashtbl.create 14 in
  Hashtbl.add table (0, 0) 0;
  Hashtbl.add table (1, 2) 9;
  Hashtbl.add table (1, 4) 7;
  Hashtbl.add table (2, 0) 8;
  Hashtbl.add table (3, 2) 15;
  Hashtbl.add table (3, 4) 12;
  Hashtbl.add table (4, 0) 10;
  table
;;

let clues_table n = if n = 9 then clues_table_9 else clues_table_5

let is_connected matrix =
  let matrix_length = Array.length matrix in
  let visited = Array.make_matrix matrix_length matrix_length false in
  let rec dfs x y =
    if x < 0
       || x >= matrix_length
       || y < 0
       || y >= matrix_length
       || visited.(x).(y)
       || matrix.(x).(y) = 0
    then ()
    else (
      visited.(x).(y) <- true;
      dfs (x - 1) y;
      dfs (x + 1) y;
      dfs x (y - 1);
      dfs x (y + 1))
  in
  let rec find_starting_cell x y =
    if x < matrix_length
    then
      if y < matrix_length
      then if matrix.(x).(y) <> 0 then x, y else find_starting_cell x (y + 1)
      else find_starting_cell (x + 1) 0
    else -1, -1
  in
  let x, y = find_starting_cell 0 0 in
  dfs x y;
  let rec check_visited x y =
    if x < matrix_length
    then
      if y < matrix_length
      then
        if matrix.(x).(y) <> 0
        then if visited.(x).(y) then check_visited x (y + 1) else false
        else check_visited x (y + 1)
      else check_visited (x + 1) 0
    else true
  in
  check_visited 0 0
;;

let get_adj_cells x y matrix =
  let matrix_length = Array.length matrix in
  let adj_cells = ref [] in
  if x - 1 >= 0 then adj_cells := (x - 1, y) :: !adj_cells else ();
  if x + 1 < matrix_length then adj_cells := (x + 1, y) :: !adj_cells else ();
  if y - 1 >= 0 then adj_cells := (x, y - 1) :: !adj_cells else ();
  if y + 1 < matrix_length then adj_cells := (x, y + 1) :: !adj_cells else ();
  !adj_cells
;;

let get_adj_cells_sum x y matrix =
  let adj_cells = get_adj_cells x y matrix in
  List.fold_left (fun acc (x, y) -> acc + matrix.(x).(y)) 0 adj_cells
;;

let get_adj_clues x y matrix =
  let adj_cells = get_adj_cells x y matrix in
  let clues =
    List.fold_left
      (fun acc (x, y) ->
        match Hashtbl.find_opt (clues_table (Array.length matrix)) (x, y) with
        | Some _ -> (x, y) :: acc
        | None -> acc)
      []
      adj_cells
  in
  Array.of_list clues
;;

let square_directions =
  [| [| -1, -1; -1, 0; 0, -1 |]
   ; [| -1, 1; -1, 0; 0, 1 |]
   ; [| 1, 1; 1, 0; 0, 1 |]
   ; [| 1, -1; 1, 0; 0, -1 |]
  |]
;;

let squares_are_valid x y matrix =
  let is_valid = ref true in
  let matrix_length = Array.length matrix in
  for i = 0 to Array.length square_directions - 1 do
    let dx, dy = square_directions.(i).(0) in
    let dx1, dy1 = square_directions.(i).(1) in
    let dx2, dy2 = square_directions.(i).(2) in
    let x1 = x + dx in
    let y1 = y + dy in
    let x2 = x + dx1 in
    let y2 = y + dy1 in
    let x3 = x + dx2 in
    let y3 = y + dy2 in
    if x1 < 0
       || x1 >= matrix_length
       || y1 < 0
       || y1 >= matrix_length
       || x2 < 0
       || x2 >= matrix_length
       || y2 < 0
       || y2 >= matrix_length
       || x3 < 0
       || x3 >= matrix_length
       || y3 < 0
       || y3 >= matrix_length
    then ()
    else (
      let cells = [| x1, y1; x2, y2; x3, y3 |] in
      let i = ref 0 in
      let blank_cells = ref 0 in
      while !blank_cells < 1 && !i < Array.length cells do
        let x, y = cells.(!i) in
        if matrix.(x).(y) = 0 then blank_cells := !blank_cells + 1 else ();
        i := !i + 1
      done;
      if !blank_cells = 0 then is_valid := false else ())
  done;
  !is_valid
;;

let is_clue_valid x y matrix f =
  let adj_cells_sum = get_adj_cells_sum x y matrix in
  match Hashtbl.find_opt (clues_table (Array.length matrix)) (x, y) with
  | Some clue_target_value -> f clue_target_value adj_cells_sum
  | None -> true
;;

let clues_are_valid clues_table matrix =
  let all_valid = ref true in
  Hashtbl.iter
    (fun (x, y) _ ->
      let is_valid =
        is_clue_valid x y matrix (fun clue_target_value adj_cells_sum ->
          if adj_cells_sum = clue_target_value then true else false)
      in
      if not is_valid then all_valid := false else ())
    clues_table;
  !all_valid
;;

let get_all_clues_valid num adj_clues matrix =
  let all_valid = ref true in
  let i = ref 0 in
  while !all_valid && !i < Array.length adj_clues do
    let x, y = adj_clues.(!i) in
    let is_valid =
      is_clue_valid x y matrix (fun clue_target_value adj_cells_sum ->
        if adj_cells_sum + num <= clue_target_value then true else false)
    in
    if not is_valid then all_valid := false else ();
    i := !i + 1
  done;
  !all_valid
;;

let get_shapes matrix =
  let matrix_length = Array.length matrix in
  let shapes = Array.make matrix_length [] in
  let clues = clues_table matrix_length in
  for i = 0 to matrix_length - 1 do
    for j = 0 to matrix_length - 1 do
      let value = matrix.(i).(j) in
      if value <> 0 && not (Hashtbl.mem clues (i, j))
      then shapes.(value - 1) <- (i, j) :: shapes.(value - 1)
      else ()
    done
  done;
  Array.to_list shapes
;;

let rec fill_l_shape cur_num num_left nums cells l_shapes max_num matrix =
  let cells_left = List.length cells in
  (* Check we have more or equal cells to what we have to fill. *)
  if num_left > cells_left
  then None
  else if num_left = 0 && List.length l_shapes = 0
  then (
    (* We filled all the cells for the last L-Shape so we are done. *)
    let clues_valid = clues_are_valid (clues_table (Array.length matrix)) matrix in
    if clues_valid
    then (
      let matrix_connected = is_connected matrix in
      if matrix_connected
      then (
        output_to_file matrix;
        Some matrix)
      else None)
    else None)
  else if num_left = 0
  then (
    (* We filled all the cells for this L-Shape so move on to the next L-Shape. *)
    match l_shapes with
    | [] -> None
    | new_cells :: rest_l_shapes ->
      let i = ref 0 in
      let result = ref None in
      while !i < List.length nums && !result = None do
        let new_num = List.nth nums !i in
        let rest_nums = List.filter (fun x -> x <> new_num) nums in
        if cur_num = 5 && new_num = 3 then () else ();
        result
        := fill_l_shape new_num new_num rest_nums new_cells rest_l_shapes max_num matrix;
        i := !i + 1
      done;
      !result)
  else (
    (* Get the first cell of the L-Shape *)
    let result = ref None in
    let rest_cells = ref cells in
    while !result = None && List.length !rest_cells >= 1 do
      let x, y = List.hd !rest_cells in
      rest_cells := List.tl !rest_cells;
      if cur_num = 3 then () else ();
      (* Check if clues are valid *)
      let adj_clues = get_adj_clues x y matrix in
      let all_clues_valid = get_all_clues_valid cur_num adj_clues matrix in
      if all_clues_valid = true
      then (
        (* Check if squares a valid *)
        let squares_valid = squares_are_valid x y matrix in
        if squares_valid = true
        then (
          (* Fill current cell *)
          matrix.(x).(y) <- cur_num;
          (* Check if we can fill the rest of the shape *)
          let sub_result =
            fill_l_shape cur_num (num_left - 1) nums !rest_cells l_shapes max_num matrix
          in
          if Option.is_none sub_result
          then (* Backtrack and remove assignment *)
            matrix.(x).(y) <- 0
          else result := sub_result)
        else ())
      else ()
    done;
    !result)
;;

let find_solution matrix_shape =
  (* print_matrix matrix_shape; *)
  let matrix_size = Array.length matrix_shape in
  let matrix = Array.make_matrix matrix_size matrix_size 0 in
  let l_shapes = get_shapes matrix_shape in
  (* print_l_shapes l_shapes; *)
  let nums = if matrix_size = 5 then [ 2; 3; 4; 5 ] else [ 2; 3; 4; 5; 6; 7; 8; 9 ] in
  let cells = List.hd l_shapes in
  let rest_l_shapes = List.tl l_shapes in
  let res = fill_l_shape 1 1 nums cells rest_l_shapes matrix_size matrix in
  res
;;
