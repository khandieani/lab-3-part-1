
int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <search-term>\n", argv[0]);
        exit(1);
    }

    int pipe1[2]; // Pipe between P1 (cat scores) and P2 (grep)
    int pipe2[2]; // Pipe between P2 (grep) and P3 (sort)

    // Create the first pipe
    if (pipe(pipe1) == -1) {
        perror("pipe1");
        exit(1);
    }

    // Fork the first child process (P2 - grep)
    pid_t pid1 = fork();
    if (pid1 < 0) {
        perror("fork");
        exit(1);
    }

    if (pid1 == 0) {
        // In child process P2 (grep)

        // Redirect pipe1's read end to stdin
        dup2(pipe1[0], STDIN_FILENO);
        close(pipe1[0]);
        close(pipe1[1]); // Close unused write end

        // Create the second pipe
        if (pipe(pipe2) == -1) {
            perror("pipe2");
            exit(1);
        }

        // Fork the second child process (P3 - sort)
        pid_t pid2 = fork();
        if (pid2 < 0) {
            perror("fork");
            exit(1);
        }

        if (pid2 == 0) {
            // In child process P3 (sort)

            // Redirect pipe2's read end to stdin
            dup2(pipe2[0], STDIN_FILENO);
            close(pipe2[0]);
            close(pipe2[1]); // Close unused write end

            // Execute the `sort` command
            execlp("sort", "sort", NULL);
            perror("execlp sort");
            exit(1);
        } else {
            // In child process P2 (grep)

            // Redirect stdout to pipe2's write end
            dup2(pipe2[1], STDOUT_FILENO);
            close(pipe2[0]);
            close(pipe2[1]); // Close unused read end

            // Execute the `grep` command with the search term
            execlp("grep", "grep", argv[1], NULL);
            perror("execlp grep");
            exit(1);
        }
    } else {
        // In parent process P1 (cat scores)

        // Redirect stdout to pipe1's write end
        dup2(pipe1[1], STDOUT_FILENO);
        close(pipe1[0]);
        close(pipe1[1]); // Close unused read end

        // Execute the `cat scores` command
        execlp("cat", "cat", "scores", NULL);
        perror("execlp cat");
        exit(1);
    }

    return 0;
}
