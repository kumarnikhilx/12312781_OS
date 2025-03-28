import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUSchedulingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced CPU Scheduling Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")

        # Variables
        self.num_processes = tk.IntVar(value=3)
        self.scheduling_algorithm = tk.StringVar(value="FCFS")
        self.time_quantum = tk.IntVar(value=2)
        self.process_data = []

        # GUI Setup
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Input Frame
        self.input_frame = tk.LabelFrame(self.main_frame, text="Process Input", bg="#ffffff", padx=10, pady=10)
        self.input_frame.pack(fill="x", padx=5, pady=5)

        # Algorithm Selection Frame
        self.algorithm_frame = tk.LabelFrame(self.main_frame, text="Scheduling Algorithm", bg="#ffffff", padx=10, pady=10)
        self.algorithm_frame.pack(fill="x", padx=5, pady=5)

        # Gantt Chart Frame
        self.gantt_frame = tk.LabelFrame(self.main_frame, text="Gantt Chart", bg="#ffffff", padx=10, pady=10)
        self.gantt_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Setup Input Fields
        self.setup_input_fields()
        self.setup_algorithm_selection()
        self.setup_results_area()

    def setup_input_fields(self):
        # Number of Processes
        tk.Label(self.input_frame, text="Number of Processes:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        spinbox = tk.Spinbox(self.input_frame, from_=1, to=10, textvariable=self.num_processes, width=5, command=self.update_process_table)
        spinbox.grid(row=0, column=1, padx=5, pady=5)
        spinbox.bind("<Return>", lambda e: self.update_process_table())

        # Process Table Frame
        self.table_frame = tk.Frame(self.input_frame, bg="#ffffff")
        self.table_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        # Create headers
        tk.Label(self.table_frame, text="Process", bg="#ffffff", width=10).grid(row=0, column=0)
        tk.Label(self.table_frame, text="Arrival Time", bg="#ffffff", width=10).grid(row=0, column=1)
        tk.Label(self.table_frame, text="Burst Time", bg="#ffffff", width=10).grid(row=0, column=2)
        tk.Label(self.table_frame, text="Priority", bg="#ffffff", width=10).grid(row=0, column=3)

        # Initialize entry lists
        self.process_labels = []
        self.arrival_entries = []
        self.burst_entries = []
        self.priority_entries = []

        # Populate initial processes
        self.update_process_table()

    def update_process_table(self):
        # Clear existing widgets
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:  # Keep headers
                widget.destroy()
        
        self.process_labels.clear()
        self.arrival_entries.clear()
        self.burst_entries.clear()
        self.priority_entries.clear()

        # Add new rows
        for i in range(self.num_processes.get()):
            # Process label
            label = tk.Label(self.table_frame, text=f"P{i+1}", bg="#ffffff", width=10)
            label.grid(row=i+1, column=0)
            self.process_labels.append(label)

            # Arrival time entry
            arrival_var = tk.StringVar(value="0")
            arrival_entry = tk.Entry(self.table_frame, textvariable=arrival_var, width=10)
            arrival_entry.grid(row=i+1, column=1)
            self.arrival_entries.append(arrival_var)

            # Burst time entry
            burst_var = tk.StringVar(value="1")
            burst_entry = tk.Entry(self.table_frame, textvariable=burst_var, width=10)
            burst_entry.grid(row=i+1, column=2)
            self.burst_entries.append(burst_var)

            # Priority entry
            priority_var = tk.StringVar(value="0")
            priority_entry = tk.Entry(self.table_frame, textvariable=priority_var, width=10)
            priority_entry.grid(row=i+1, column=3)
            self.priority_entries.append(priority_var)

    def setup_algorithm_selection(self):
        # Algorithm Selection
        algorithms = ["FCFS", "SJF (Non-Preemptive)", "Priority (Non-Preemptive)", "Round Robin", "SRTF (Preemptive)"]
        ttk.Combobox(self.algorithm_frame, textvariable=self.scheduling_algorithm, values=algorithms, state="readonly").grid(row=0, column=0, padx=5, pady=5)

        # Time Quantum (for Round Robin)
        tk.Label(self.algorithm_frame, text="Time Quantum (for RR):", bg="#ffffff").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        tk.Entry(self.algorithm_frame, textvariable=self.time_quantum, width=5).grid(row=0, column=2, padx=5, pady=5)

        # Calculate Button
        tk.Button(self.algorithm_frame, text="Run Simulation", command=self.run_simulation, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)

    def setup_results_area(self):
        # Results Text Area
        self.results_text = tk.Text(self.gantt_frame, height=10, width=80)
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Matplotlib Figure
        self.figure = plt.Figure(figsize=(8, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.gantt_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def run_simulation(self):
        # Get process data from entry widgets
        self.process_data = []
        for i in range(self.num_processes.get()):
            try:
                arrival = int(self.arrival_entries[i].get())
                burst = int(self.burst_entries[i].get())
                priority = int(self.priority_entries[i].get())
                
                if burst <= 0:
                    messagebox.showerror("Error", "Burst time must be positive")
                    return
                
                self.process_data.append({
                    "pid": f"P{i+1}",
                    "arrival": arrival,
                    "burst": burst,
                    "priority": priority
                })
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for all fields")
                return

        # Run selected algorithm
        algorithm = self.scheduling_algorithm.get()
        if algorithm == "FCFS":
            results = self.fcfs()
        elif algorithm == "SJF (Non-Preemptive)":
            results = self.sjf_non_preemptive()
        elif algorithm == "Priority (Non-Preemptive)":
            results = self.priority_non_preemptive()
        elif algorithm == "Round Robin":
            results = self.round_robin()
        elif algorithm == "SRTF (Preemptive)":
            results = self.srtf_preemptive()
        else:
            messagebox.showerror("Error", "Invalid algorithm selected")
            return

        # Display results
        self.display_results(results)

    def fcfs(self):
        # Sort by arrival time
        processes = sorted(self.process_data, key=lambda x: x["arrival"])
        
        # Calculate completion, turnaround, waiting times
        current_time = 0
        results = []
        for p in processes:
            if current_time < p["arrival"]:
                current_time = p["arrival"]
            
            completion = current_time + p["burst"]
            turnaround = completion - p["arrival"]
            waiting = turnaround - p["burst"]
            
            results.append({
                "pid": p["pid"],
                "arrival": p["arrival"],
                "burst": p["burst"],
                "start": current_time,
                "finish": completion,
                "turnaround": turnaround,
                "waiting": waiting
            })
            
            current_time = completion
        
        return results

    def sjf_non_preemptive(self):
        # Sort by burst time (then arrival)
        processes = sorted(self.process_data, key=lambda x: (x["burst"], x["arrival"]))
        
        current_time = 0
        results = []
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available = [p for p in remaining_processes if p["arrival"] <= current_time]
            
            if not available:
                current_time += 1
                continue
            
            # Select shortest job
            next_process = min(available, key=lambda x: x["burst"])
            remaining_processes.remove(next_process)
            
            completion = current_time + next_process["burst"]
            turnaround = completion - next_process["arrival"]
            waiting = turnaround - next_process["burst"]
            
            results.append({
                "pid": next_process["pid"],
                "arrival": next_process["arrival"],
                "burst": next_process["burst"],
                "start": current_time,
                "finish": completion,
                "turnaround": turnaround,
                "waiting": waiting
            })
            
            current_time = completion
        
        return results

    def priority_non_preemptive(self):
        # Sort by priority (lower number = higher priority)
        processes = sorted(self.process_data, key=lambda x: (x["priority"], x["arrival"]))
        
        current_time = 0
        results = []
        remaining_processes = processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived
            available = [p for p in remaining_processes if p["arrival"] <= current_time]
            
            if not available:
                current_time += 1
                continue
            
            # Select highest priority (lowest number)
            next_process = min(available, key=lambda x: x["priority"])
            remaining_processes.remove(next_process)
            
            completion = current_time + next_process["burst"]
            turnaround = completion - next_process["arrival"]
            waiting = turnaround - next_process["burst"]
            
            results.append({
                "pid": next_process["pid"],
                "arrival": next_process["arrival"],
                "burst": next_process["burst"],
                "priority": next_process["priority"],
                "start": current_time,
                "finish": completion,
                "turnaround": turnaround,
                "waiting": waiting
            })
            
            current_time = completion
        
        return results

    def round_robin(self):
        time_quantum = self.time_quantum.get()
        processes = sorted(self.process_data, key=lambda x: x["arrival"])
        
        current_time = 0
        results = []
        remaining_burst = {p["pid"]: p["burst"] for p in processes}
        queue = []
        
        while any(remaining_burst.values()):
            # Add arriving processes to queue
            for p in processes:
                if p["arrival"] == current_time and p["pid"] not in [x["pid"] for x in queue]:
                    queue.append({
                        "pid": p["pid"],
                        "arrival": p["arrival"],
                        "burst": p["burst"]
                    })
            
            if not queue:
                current_time += 1
                continue
            
            # Get next process
            current_process = queue.pop(0)
            pid = current_process["pid"]
            
            # Execute for time quantum or remaining burst
            execution_time = min(time_quantum, remaining_burst[pid])
            
            # Record start time if first execution
            if remaining_burst[pid] == current_process["burst"]:
                start_time = current_time
            
            # Update remaining burst
            remaining_burst[pid] -= execution_time
            
            # Update current time
            current_time += execution_time
            
            # If process completed
            if remaining_burst[pid] == 0:
                completion = current_time
                arrival = next(p["arrival"] for p in processes if p["pid"] == pid)
                burst = current_process["burst"]
                
                results.append({
                    "pid": pid,
                    "arrival": arrival,
                    "burst": burst,
                    "start": start_time,
                    "finish": completion,
                    "turnaround": completion - arrival,
                    "waiting": (completion - arrival) - burst
                })
            else:
                # Re-add to queue if not finished
                queue.append(current_process)
        
        return results

    def srtf_preemptive(self):
        processes = sorted(self.process_data, key=lambda x: x["arrival"])
        
        current_time = 0
        results = []
        remaining_burst = {p["pid"]: p["burst"] for p in processes}
        last_execution = {p["pid"]: None for p in processes}
        
        while any(remaining_burst.values()):
            # Find processes that have arrived and have remaining burst
            available = [p for p in processes 
                        if p["arrival"] <= current_time and remaining_burst[p["pid"]] > 0]
            
            if not available:
                current_time += 1
                continue
            
            # Select process with shortest remaining time
            next_process = min(available, key=lambda x: remaining_burst[x["pid"]])
            pid = next_process["pid"]
            
            # If this is the first time the process is running
            if last_execution[pid] is None:
                last_execution[pid] = {"start": current_time}
            
            # Execute for 1 time unit (preemptive)
            remaining_burst[pid] -= 1
            current_time += 1
            
            # If process completed
            if remaining_burst[pid] == 0:
                arrival = next_process["arrival"]
                burst = next_process["burst"]
                start = last_execution[pid]["start"]
                
                results.append({
                    "pid": pid,
                    "arrival": arrival,
                    "burst": burst,
                    "start": start,
                    "finish": current_time,
                    "turnaround": current_time - arrival,
                    "waiting": (current_time - arrival) - burst
                })
        
        return results

    def display_results(self, results):
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.ax.clear()
        
        # Display textual results
        self.results_text.insert(tk.END, f"{self.scheduling_algorithm.get()} Scheduling Results:\n\n")
        self.results_text.insert(tk.END, "PID\tArrival\tBurst\tStart\tFinish\tTurnaround\tWaiting\n")
        self.results_text.insert(tk.END, "-"*70 + "\n")
        
        total_turnaround = 0
        total_waiting = 0
        
        for r in results:
            self.results_text.insert(tk.END, 
                f"{r['pid']}\t{r['arrival']}\t{r['burst']}\t{r['start']}\t{r['finish']}\t{r['turnaround']}\t\t{r['waiting']}\n")
            total_turnaround += r["turnaround"]
            total_waiting += r["waiting"]
        
        avg_turnaround = total_turnaround / len(results)
        avg_waiting = total_waiting / len(results)
        
        self.results_text.insert(tk.END, "\nAverage Turnaround Time: {:.2f}\n".format(avg_turnaround))
        self.results_text.insert(tk.END, "Average Waiting Time: {:.2f}\n".format(avg_waiting))
        
        # Generate Gantt chart
        self.generate_gantt_chart(results)

    def generate_gantt_chart(self, results):
        self.ax.clear()
        
        # Sort by start time
        results_sorted = sorted(results, key=lambda x: x["start"])
        
        # Create bars
        for i, r in enumerate(results_sorted):
            duration = r["finish"] - r["start"]
            self.ax.broken_barh([(r["start"], duration)], (10 - i, 0.8), facecolors=f"C{i}")
            self.ax.text(r["start"] + duration/2, 10 - i + 0.4, r["pid"], ha="center", va="center", color="white")
        
        # Formatting
        self.ax.set_yticks([10 - i + 0.4 for i in range(len(results_sorted))])
        self.ax.set_yticklabels([r["pid"] for r in results_sorted])
        self.ax.set_xlabel("Time")
        self.ax.set_title(f"{self.scheduling_algorithm.get()} Scheduling Gantt Chart")
        self.ax.grid(True)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulingSimulator(root)
    root.mainloop()