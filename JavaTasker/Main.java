import java.util.Scanner;
import java.util.List;

public class Main {
    private static TaskManager taskManager = new TaskManager();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        while (true) {
            displayMenu();
            int choice = getIntInput("Enter your choice: ");

            switch (choice) {
                case 1:
                    addNewTask();
                    break;
                case 2:
                    removeTask();
                    break;
                case 3:
                    markTaskComplete();
                    break;
                case 4:
                    viewAllTasks();
                    break;
                case 5:
                    System.out.println("Goodbye!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    private static void displayMenu() {
        System.out.println("\n=== Task Manager ===");
        System.out.println("1. Add New Task");
        System.out.println("2. Remove Task");
        System.out.println("3. Mark Task as Complete");
        System.out.println("4. View All Tasks");
        System.out.println("5. Exit");
    }

    private static void addNewTask() {
        System.out.println("\nAdd New Task");
        System.out.print("Enter title: ");
        String title = scanner.nextLine();
        System.out.print("Enter description: ");
        String description = scanner.nextLine();
        System.out.print("Enter due date: ");
        String dueDate = scanner.nextLine();

        Task task = new Task(title, description, dueDate);
        taskManager.addTask(task);
        System.out.println("Task added successfully!");
    }

    private static void removeTask() {
        viewAllTasks();
        int index = getIntInput("Enter task number to remove: ") - 1;
        taskManager.removeTask(index);
        System.out.println("Task removed successfully!");
    }

    private static void markTaskComplete() {
        viewAllTasks();
        int index = getIntInput("Enter task number to mark as complete: ") - 1;
        taskManager.markTaskComplete(index);
        System.out.println("Task marked as complete!");
    }

    private static void viewAllTasks() {
        List<Task> tasks = taskManager.getAllTasks();
        if (tasks.isEmpty()) {
            System.out.println("\nNo tasks found.");
            return;
        }

        System.out.println("\nAll Tasks:");
        for (int i = 0; i < tasks.size(); i++) {
            System.out.println("\n" + (i + 1) + ". " + tasks.get(i));
        }
    }

    private static int getIntInput(String prompt) {
        while (true) {
            try {
                System.out.print(prompt);
                return Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
            }
        }
    }
}