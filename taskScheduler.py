import heapq
import json
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
import time
import pygame
import winsound
from plyer import notification



class TaskScheduler:
    def __init__(self):
        self.task_heap = []
        self.load_tasks()

    def add_task(self, priority, task_name, date, time):
        deadline_timestamp = self._convert_deadline_to_timestamp(date, time)
        heapq.heappush(self.task_heap, (priority, deadline_timestamp, task_name))
        self.save_tasks()

    def edit_task(self, old_task_name, new_task_name, priority, date, time):
        self.task_heap = [(p, d, t) for p, d, t in self.task_heap if t != old_task_name]
        heapq.heapify(self.task_heap)
        self.add_task(priority, new_task_name, date, time)

    def delete_task(self, task_name):
        self.task_heap = [(p, d, t) for p, d, t in self.task_heap if t != task_name]
        heapq.heapify(self.task_heap)
        self.save_tasks()

    def execute_task(self):
        if self.task_heap:
            task = heapq.heappop(self.task_heap)
            self.save_tasks()
            return task
        return None

    def get_all_tasks(self, sort_by="priority"):
        if sort_by == "deadline":
            return sorted(self.task_heap, key=lambda x: x[1])  # Sort by deadline
        return sorted(self.task_heap)  # Sort by priority

    def save_tasks(self):
        tasks = [{"priority": p, "deadline": d, "task_name": t} for p, d, t in self.task_heap]
        with open("../tasks.json", "w") as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open("../tasks.json", "r") as f:
                tasks = json.load(f)
                for task in tasks:
                    heapq.heappush(self.task_heap, (task["priority"], task["deadline"], task["task_name"]))
        except FileNotFoundError:
            pass

    @staticmethod
    def _convert_deadline_to_timestamp(date, time):
        try:
            deadline_str = f"{date} {time}"
            return datetime.strptime(deadline_str, "%d/%m/%Y %H:%M").timestamp()
        except ValueError:
            return float("inf") 


class SchedulerApp:
    def __init__(self, root):
        self.scheduler = TaskScheduler()


        if pygame:
            pygame.mixer.init()

        root.title("Task Scheduler")
        root.geometry("800x800")
        root.configure(bg="#282C34")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#E94560", foreground="white", font=("Arial", 12, "bold"))
        self.style.configure("TLabel", background="#282C34", foreground="white", font=("Arial", 12))
        self.style.configure("Treeview", background="#2E2E2E", foreground="white", font=("Arial", 12), rowheight=30)
        self.style.configure("Treeview.Heading", background="#1F2329", foreground="white", font=("Arial", 12, "bold"))

        # Header
        Label(root, text="✨ Task Scheduler ✨", font=("Helvetica", 24, "bold"), bg="#282C34", fg="#E94560").pack(pady=10)

        # Inputs
        self.task_name_var = StringVar()
        self.priority_var = StringVar()
        self.date_var = StringVar()
        self.time_var = StringVar()

        self._create_input_section(root)
        self._create_task_list_section(root)
        self._create_buttons(root)
        self._create_notification_section(root)

        self.update_task_list()

        threading.Thread(target=self.check_notifications, daemon=True).start()

    def _create_input_section(self, root):
        input_frame = Frame(root, bg="#282C34")
        input_frame.pack(pady=10)

        Label(input_frame, text="Task Name:", bg="#282C34", fg="white", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                 padx=10, pady=5,
                                                                                                 sticky=W)
        Entry(input_frame, textvariable=self.task_name_var, width=25, font=("Arial", 12)).grid(row=0, column=1, padx=10,
                                                                                               pady=5)

        Label(input_frame, text="Priority:", bg="#282C34", fg="white", font=("Arial", 12)).grid(row=1, column=0,
                                                                                                padx=10, pady=5,
                                                                                                sticky=W)
        Entry(input_frame, textvariable=self.priority_var, width=25, font=("Arial", 12)).grid(row=1, column=1, padx=10,
                                                                                              pady=5)

        Label(input_frame, text="Date (DD/MM/YYYY):", bg="#282C34", fg="white", font=("Arial", 12)).grid(row=2,
                                                                                                         column=0,
                                                                                                         padx=10,
                                                                                                         pady=5,
                                                                                                         sticky=W)
        Entry(input_frame, textvariable=self.date_var, width=25, font=("Arial", 12)).grid(row=2, column=1, padx=10,
                                                                                          pady=5)

        Label(input_frame, text="Time (HH:MM):", bg="#282C34", fg="white", font=("Arial", 12)).grid(row=3, column=0,
                                                                                                    padx=10, pady=5,
                                                                                                    sticky=W)
        Entry(input_frame, textvariable=self.time_var, width=25, font=("Arial", 12)).grid(row=3, column=1, padx=10,
                                                                                          pady=5)

    def _create_task_list_section(self, root):
        self.tree = ttk.Treeview(root, columns=("priority", "deadline", "task"), show="headings")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("deadline", text="Deadline")
        self.tree.heading("task", text="Task Name")
        self.tree.pack(pady=20, fill=BOTH, expand=True)

    def _create_buttons(self, root):
        button_frame = Frame(root, bg="#282C34")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Execute Task", command=self.execute_task).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Edit Task", command=self.edit_task).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=3, padx=10, pady=10)

    def _create_notification_section(self, root):
        notification_frame = Frame(root, bg="#282C34")
        notification_frame.pack(pady=10)
        self.notification_label = Label(notification_frame, text="", bg="#282C34", fg="#E94560", font=("Arial", 12))
        self.notification_label.pack()

    def add_task(self):
        task_name = self.task_name_var.get()
        priority = self.priority_var.get()
        date = self.date_var.get()
        time = self.time_var.get()
        try:
            priority = int(priority)
            self.scheduler.add_task(priority, task_name, date, time)
            self.update_task_list()
            self.task_name_var.set('')
            self.priority_var.set('')
            self.date_var.set('')
            self.time_var.set('')
            messagebox.showinfo("Success", f"Task '{task_name}' added.")
        except ValueError:
            messagebox.showerror("Error", "Invalid priority or deadline.")

    def execute_task(self):
        task = self.scheduler.execute_task()
        if task:
            messagebox.showinfo("Task Executed", f"Executed Task: {task[2]} (Priority: {task[0]})")
            self.update_task_list()
        else:
            messagebox.showerror("Error", "No tasks to execute.")

    def edit_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            old_task_name = self.tree.item(selected_item, "values")[2]
            new_task_name = self.task_name_var.get()
            priority = self.priority_var.get()
            date = self.date_var.get()
            time = self.time_var.get()
            try:
                priority = int(priority)
                self.scheduler.edit_task(old_task_name, new_task_name, priority, date, time)
                self.update_task_list()
                messagebox.showinfo("Success", f"Task '{old_task_name}' updated.")
            except ValueError:
                messagebox.showerror("Error", "Invalid priority or deadline.")
        else:
            messagebox.showerror("Error", "No task selected.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_name = self.tree.item(selected_item, "values")[2]
            self.scheduler.delete_task(task_name)
            self.update_task_list()
            messagebox.showinfo("Success", f"Task '{task_name}' deleted.")
        else:
            messagebox.showerror("Error", "No task selected.")

    def update_task_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tasks = self.scheduler.get_all_tasks("priority")
        for priority, deadline, task_name in tasks:
            deadline_str = datetime.fromtimestamp(deadline).strftime("%m/%d/%Y %H:%M") if deadline != float(
                "inf") else "No Deadline"
            self.tree.insert("", END, values=(priority, deadline_str, task_name))

    def check_notifications(self):
        while True:
            now = datetime.now().timestamp()
            upcoming_tasks = [(p, d, t) for p, d, t in self.scheduler.task_heap if d - now <= 60 and d > now]

            for task in upcoming_tasks:
                self.notification_label.config(text=f"Task '{task[2]}' is nearing its deadline!")

                notification_title = "Task Deadline Approaching!"
                notification_message = f"Task '{task[2]}' is nearing its deadline."

                notification.notify(
                    title=notification_title,
                    message=notification_message,
                    timeout=10
                )

                self._play_notification_sound()

            time.sleep(60)

    def _play_notification_sound(self):
        if pygame:
            sound = pygame.mixer.Sound('../notification.mp3')
            sound.play()
        else:
            winsound.Beep(1000, 1000)

if __name__ == "__main__":
    root = Tk()
    app = SchedulerApp(root)
    root.mainloop()
