module T = Domainslib.Task

let parse_matrices filename =
  let file = open_in filename in
  let rec parse_matrix acc =
    try
      let line = input_line file in
      match line with
      | "" -> raise Exit
      | _ ->
        let row =
          Array.map int_of_string (Array.of_list (String.split_on_char ' ' line))
        in
        parse_matrix (row :: acc)
    with
    | Exit -> Array.of_list (List.rev acc)
  in
  let rec parse_matrices acc =
    try
      let matrix = parse_matrix [] in
      parse_matrices (matrix :: acc)
    with
    | End_of_file -> acc
  in
  let matrices = parse_matrices [] in
  close_in file;
  matrices
;;

let get_num_cpus () =
  let open Unix in
  let ocaml_stdout, _, _ = open_process_full "/usr/sbin/sysctl -n hw.ncpu" [||] in
  let num_cpus = int_of_string (input_line ocaml_stdout) in
  print_string ("Number of CPUs: " ^ string_of_int num_cpus ^ "\n");
  if num_cpus < 0 then 2 else num_cpus
;;

let () =
  let matrix_size = int_of_string Sys.argv.(1) in
  let matrices = parse_matrices (Format.sprintf "./data/all_shapes_%i.txt" matrix_size) in
  print_string "Matrices parsed\n";
  let num_domains = get_num_cpus () - 1 in
  let pool = T.setup_pool ~num_domains () in
  T.run pool (fun () ->
    T.parallel_for
      pool
      ~start:0
      ~finish:(List.length matrices - 1)
      ~body:(fun i ->
        let matrix = List.nth matrices i in
        let result = Solution.find_solution matrix in
        match result with
        | Some matrix ->
          print_string "Solution found\n";
          Solution.output_to_file matrix
        | None -> ()))
;;
