from robot import Robot


def parse_problem(world_file, problem_file):
    current_obstacles, current_problems = [], []

    # 2 coordinates for 2d problem
    n = 2

    # first line is the robot
    is_robot = 0
    with open(world_file) as f:
        for current_line in f.readlines():
            current_line = list(map(float, current_line.split()))
            current_line = [current_line[i: i + n] for i in range(0, len(current_line), n)]
            if not is_robot:
                r = Robot(current_line[0][0], current_line[0][1])
                is_robot += 1
            else:
                current_obstacles.append(tuple(current_line))

    with open(problem_file, "r") as f:
        for current_line in f.readlines():
            current_line = list(map(float, current_line.split()))
            current_line = [current_line[i: i + n] for i in range(0, len(current_line), n)]
            current_problems.append(tuple(current_line))

    return [r, current_obstacles, current_problems]


if __name__ == '__main__':
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    qx, qy = 0, 0
    robot, obstacles, problems = parse_problem(world, problem)
    robot.set_pose((0, 0, 0))
    robot.transform()
    print(robot.translated_robot)
