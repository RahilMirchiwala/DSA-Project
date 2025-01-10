# DSA-Project


# ✨ Task Scheduler

A Python-based **Task Scheduler Application** with a user-friendly interface to manage tasks effectively. This project allows users to add, edit, delete, and execute tasks with prioritization and optional deadlines. Notifications alert users of tasks nearing their deadlines.

---

## 🚀 Features

1. **Task Management**:
   - Add tasks with priority and optional deadlines.
   - Edit, delete, and execute tasks.
   - Tasks are stored persistently in a JSON file.

2. **User Interface**:
   - Built with **Tkinter**, styled using **ttk** for a modern appearance.
   - Task list displayed using a sortable **Treeview** widget.

3. **Priority Queue**:
   - Tasks are organized by priority using a **min-heap**.

4. **Notifications**:
   - Background thread alerts users when a task deadline is approaching (1-minute notice).
   - Notifications include a sound alert (using `pygame` or `winsound`).

5. **Persistence**:
   - Tasks are saved locally in `tasks.json` and reloaded on application startup.

6. **Error Handling**:
   - Input validation with helpful error messages for invalid priorities or deadlines.

---

## 📦 Prerequisites

- Python 3.7+
- The following Python libraries:
  - `heapq` (Standard Library)
  - `json` (Standard Library)
  - `tkinter` (Standard Library)
  - `threading` (Standard Library)
  - `pygame` (Install via pip: `pip install pygame`)
  - `winsound` (Windows-only, built-in)

---

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RahilMirchiwala/Task-Scheduler.git
   cd Task-Scheduler
   ```

2. Install required Python libraries:
   ```bash
   pip install pygame
   ```

3. Run the application:
   ```bash
   python task_scheduler.py
   ```

---

## 📋 Usage

1. **Add Task**:
   - Enter the task name, priority (integer), date (DD/MM/YYYY), and time (HH:MM).
   - Click **Add Task** to save it.

2. **Edit Task**:
   - Select a task from the list.
   - Modify the task details in the input fields.
   - Click **Edit Task** to update it.

3. **Delete Task**:
   - Select a task from the list.
   - Click **Delete Task** to remove it.

4. **Execute Task**:
   - Click **Execute Task** to mark the highest priority task as done.

5. **Notifications**:
   - The app will alert you when a task is nearing its deadline (within 1 minute).

---
## Screenshots

### Main GUI Layout
![Main GUI Layout]("Image/GUI.png")

### Adding a Task
![Adding a Task]("Image\Task.png")

### Notification Alert
![Notification Alert]("Imag\Notification.png")



## 📂 File Structure

```
Task-Scheduler/
│
├── task_scheduler.py  # Main application script
├── tasks.json         # Saved tasks (auto-generated)
├── notification.mp3   # Notification sound file
├── README.md          # Project documentation
```

---

## 🐛 Known Issues

- Notifications require `notification.mp3` in the project directory.
- Date and time validation could be improved with a date-picker widget.

---

## 🤝 Acknowledgments

- **Python Libraries**: tkinter, pygame
- Special thanks to the ByteXL and Gaurav Mandoli Sir for guidance.
