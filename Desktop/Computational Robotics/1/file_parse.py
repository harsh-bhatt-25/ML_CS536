def get_robot_global_coordinates(robot_config, x, y):
    rob_at_pt = []
    for idx, pt in enumerate(robot_config):
        if idx == 0:
            rob_at_pt.append((x, y))
        else:
            rob_at_pt.append((round(pt[0] + x - robot_config[0][0], 1), round(pt[1] + y - robot_config[0][1], 1)))
    return rob_at_pt


def parse_problem(world_file, problem_file):
    current_obstacles, current_problems = [], []

    # 2 coordinates for 2d problem
    n = 2

    # first line is the robot
    is_robot = 0
    current_robot = []
    with open(world_file) as f:
        for current_line in f.readlines():
            current_line = list(map(float, current_line.split()))
            current_line = [current_line[i: i + n] for i in range(0, len(current_line), n)]
            if not is_robot:
                current_robot = current_line
                is_robot += 1
            else:
                current_obstacles.append(current_line)

    with open(problem_file, "r") as f:
        for current_line in f.readlines():
            current_line = list(map(float, current_line.split()))
            current_line = [current_line[i: i + n] for i in range(0, len(current_line), n)]
            current_problems.append(current_line)

    return (current_robot, current_obstacles, current_problems)


if __name__ == '__main__':
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    qx, qy = 1, 2
    robot, obstacles, problems = parse_problem(world, problem)
    print(robot)
    print(f"Robot in global configuration is {get_robot_global_coordinates(robot, qx, qy)}")
    print(obstacles)
    print(problems)
