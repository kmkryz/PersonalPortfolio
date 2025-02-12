import java.util.ArrayList;
import java.io.*;
import java.util.List;

public class TaskManager {
    private ArrayList<Task> tasks;
    private static final String FILE_PATH = "tasks.txt";

    public TaskManager() {
        tasks = new ArrayList<>();
        loadTasksFromFile();
    }

    public void addTask(Task task) {
        tasks.add(task);
        saveTasksToFile();
    }

    public void removeTask(int index) {
        if (index >= 0 && index < tasks.size()) {
            tasks.remove(index);
            saveTasksToFile();
        }
    }

    public void markTaskComplete(int index) {
        if (index >= 0 && index < tasks.size()) {
            tasks.get(index).setCompleted(true);
            saveTasksToFile();
        }
    }

    public List<Task> getAllTasks() {
        return new ArrayList<>(tasks);
    }

    private void saveTasksToFile() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_PATH))) {
            for (Task task : tasks) {
                writer.write(String.format("%s,%s,%s,%b%n",
                    task.getTitle(),
                    task.getDescription(),
                    task.getDueDate(),
                    task.isCompleted()));
            }
        } catch (IOException e) {
            System.err.println("Error saving tasks: " + e.getMessage());
        }
    }

    private void loadTasksFromFile() {
        File file = new File(FILE_PATH);
        if (!file.exists()) return;

        try (BufferedReader reader = new BufferedReader(new FileReader(FILE_PATH))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 4) {
                    Task task = new Task(parts[0], parts[1], parts[2]);
                    task.setCompleted(Boolean.parseBoolean(parts[3]));
                    tasks.add(task);
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading tasks: " + e.getMessage());
        }
    }
}