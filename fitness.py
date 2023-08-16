import datetime
import tkinter as tk
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness App")

        self.current_bmi = None  # Initialize current_bmi
        self.current_fat_percentage = None  # Initialize current_fat_percentage

        self.title_label = tk.Label(
            root, text="Fitness Tracking App", font=("Courier", 12), bg="black", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        self.create_personal_info_section()
        self.create_body_measurement_section()
        self.create_bmi_and_fat_labels()
        self.create_buttons()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_data()

    def create_personal_info_section(self):
        personal_info_labels = ["Body Weight (kg):", "Height (cm):", "Age:"]
        self.personal_info_entries = []

        for i, label_text in enumerate(personal_info_labels):
            label = tk.Label(self.root, text=label_text)
            label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="e")

            entry = tk.Entry(self.root)
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.personal_info_entries.append(entry)

    def create_body_measurement_section(self):
        body_measurement_labels = [
            "Chest (cm):", "Waist (cm):", "Abdominals (cm):", "Hips (cm):", "Thighs (cm):", "Calves (cm):"
        ]
        self.body_measurement_entries = []

        for i, label_text in enumerate(body_measurement_labels):
            label = tk.Label(self.root, text=label_text)
            label.grid(row=i + len(self.personal_info_entries) +
                       1, column=0, padx=10, pady=5, sticky="e")

            entry = tk.Entry(self.root)
            entry.grid(row=i + len(self.personal_info_entries) +
                       1, column=1, padx=10, pady=5)
            self.body_measurement_entries.append(entry)

    # def create_bmi_and_fat_labels(self):
    #     self.bmi_label = tk.Label(self.root, text="", font=("Courier", 12))
    #     self.bmi_label.grid(row=len(self.personal_info_entries) + len(
    #         self.body_measurement_entries) + 1, column=0, columnspan=2, pady=10)

    #     self.fat_percentage_label = tk.Label(
    #         self.root, text="", font=("Courier", 12))
    #     self.fat_percentage_label.grid(row=len(self.personal_info_entries) + len(
    #         self.body_measurement_entries) + 1, column=2, columnspan=2, pady=10)

    def create_bmi_and_fat_labels(self):
        self.bmi_label = tk.Label(self.root, text="", font=("Courier", 12))
        self.bmi_label.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 1, column=0, columnspan=2, pady=10)

        self.fat_percentage_input_label = tk.Label(
            self.root, text="Fat Percentage (%):")
        self.fat_percentage_input_label.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 1, column=2, padx=10, pady=5, sticky="e")

        self.fat_percentage_entry = tk.Entry(self.root)
        self.fat_percentage_entry.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 1, column=3, padx=10, pady=5)

    def create_buttons(self):
        self.calculate_bmi_button = tk.Button(
            self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_bmi_button.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 2, column=0, padx=10, pady=10, sticky="w")

        self.graph_button = tk.Button(
            self.root, text="Show Graph", command=self.show_graph)
        self.graph_button.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 2, column=1, padx=10, pady=10, sticky="e")

        self.save_button = tk.Button(
            self.root, text="Save", command=self.save_data)
        self.save_button.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 3, column=0, padx=10, pady=10, sticky="w")

        self.reset_button = tk.Button(
            self.root, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 3, column=1, padx=5, pady=10, sticky="e")

        self.load_button = tk.Button(
            self.root, text="Load", command=self.load_data)
        self.load_button.grid(row=len(self.personal_info_entries) + len(
            self.body_measurement_entries) + 3, column=2, padx=10, pady=10, sticky="e")

    # def calculate_bmi(self):
    #     try:
    #         weight = float(self.personal_info_entries[0].get())
    #         height = float(self.personal_info_entries[1].get()) / 100
    #         age = float(self.personal_info_entries[2].get())

    #         self.current_bmi = weight / (height ** 2)
    #         self.current_fat_percentage = 1.2 * self.current_bmi + 0.23 * age - 10.8

    #         self.bmi_label.config(text=f"Your BMI: {self.current_bmi:.2f}")
    #         self.fat_percentage_label.config(
    #             text=f"Your Fat Percentage: {self.current_fat_percentage:.2f}%")

    #         self.save_data()
    #     except ValueError:
    #         print("Invalid input for weight, height, or age")

    def calculate_bmi(self):
        try:
            weight = float(self.personal_info_entries[0].get())
            height = float(self.personal_info_entries[1].get()) / 100
            age = float(self.personal_info_entries[2].get())
            # Get fat percentage from entry
            fat_percentage = float(self.fat_percentage_entry.get())

            self.current_bmi = weight / (height ** 2)
            self.current_fat_percentage = fat_percentage  # Use the entered fat percentage

            self.bmi_label.config(text=f"Your BMI: {self.current_bmi:.2f}")
            # self.fat_percentage_label.config(text=f"Your Fat Percentage: {self.current_fat_percentage:.2f}%")
            self.fat_percentage_entry.delete(0, tk.END)
            self.fat_percentage_entry.insert(0, f"{fat_percentage:.2f}")

            self.save_data()
        except ValueError:
            print("Invalid input for weight, height, age, or fat percentage")

    def show_graph(self):
        try:
            data_points = self.load_data_from_csv()

            if not data_points:
                print("No data available to create a graph.")
                return

            dates = [data_point["date"] for data_point in data_points]
            weights = [data_point["personal_info"][0]
                       for data_point in data_points]
            bmis = [data_point["bmi"] for data_point in data_points]
            fat_percentages = [data_point["fat_percentage"]
                               for data_point in data_points]

            # Extract body measurements from input fields
            body_measurement_labels = [
                "Chest (cm):", "Waist (cm):", "Abdominals (cm):", "Hips (cm):", "Thighs (cm):", "Calves (cm):"]
            num_measurements = len(body_measurement_labels)
            measurements = [[data_point["measurements"][i]
                             for data_point in data_points] for i in range(num_measurements)]

            fig, ax1 = plt.subplots(figsize=(10, 6))
            ax1.plot(dates, weights, marker='o',
                     label='Weight (kg)', color='tab:blue')
            ax1.plot(dates, bmis, marker='o', label='BMI', color='tab:orange')

            ax2 = ax1.twinx()
            ax2.plot(dates, fat_percentages, marker='o',
                     label='Fat Percentage (%)', color='tab:green')

            ax3 = ax1.twinx()  # Create a new y-axis for body measurements

            # Position ax3 to the right of ax2
            ax3.spines['right'].set_position(('outward', 60))

            for i in range(num_measurements):
                ax3.plot(dates, measurements[i], marker='o',
                         label=body_measurement_labels[i], color='tab:red')

            ax1.set_xlabel("Date and Time")
            ax1.set_ylabel("Weight (kg) / BMI", color='tab:blue')
            ax2.set_ylabel("Fat Percentage (%)", color='tab:green')
            # New y-axis for body measurements
            ax3.set_ylabel("Body Measurements (CM)", color='tab:red')
            plt.title("Weight, BMI, and Fat Percentage Over Time")

            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            lines3, labels3 = ax3.get_legend_handles_labels()
            ax3.legend(lines1 + lines2 + lines3, labels1 +
                       labels2 + labels3, loc='upper left')

            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            print("No data available to create a graph.")

    def save_data(self):
        try:
            personal_info = [entry.get()
                             for entry in self.personal_info_entries]
            body_measurements = [entry.get()
                                 for entry in self.body_measurement_entries]

            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_to_save = [current_datetime, self.current_bmi,
                            self.current_fat_percentage] + personal_info + body_measurements

            with open('fitness_data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data_to_save)

            print("Data Saved to CSV file")
        except ValueError:
            print("Error while saving data to CSV file")

    def load_data(self):
        try:
            data_points = self.load_data_from_csv()

            if not data_points:
                print("No previous data found")
                return

            last_entry = data_points[-1]
            personal_info = last_entry["personal_info"]
            measurements = last_entry["measurements"]

            for entry, field in zip(personal_info + measurements, self.personal_info_entries + self.body_measurement_entries):
                field.delete(0, tk.END)
                field.insert(0, entry)

            self.current_bmi = last_entry["bmi"]
            self.bmi_label.config(text=f"Your BMI: {self.current_bmi:.2f}")

            print("Data Loaded from CSV file")
        except FileNotFoundError:
            print("No previous data found")

    def load_data_from_csv(self):
        try:
            with open('fitness_data.csv', mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if not rows:
                    return []

                data_points = []
                for row in rows[1:]:
                    date = datetime.datetime.strptime(
                        row[0], "%Y-%m-%d %H:%M:%S")
                    bmi = float(row[1]) if row[1] else 0.0
                    fat_percentage = float(row[2]) if row[2] else 0.0
                    personal_info = [
                        float(val) if val else 0.0 for val in row[3:6]]
                    measurements = [
                        float(val) if val else 0.0 for val in row[6:]]
                    data_points.append({
                        "date": date,
                        "bmi": bmi,
                        "fat_percentage": fat_percentage,
                        "personal_info": personal_info,
                        "measurements": measurements
                    })
                return data_points
        except FileNotFoundError:
            return []

    def reset_fields(self):
        for entry in self.personal_info_entries:
            entry.delete(0, tk.END)
        for entry in self.body_measurement_entries:
            entry.delete(0, tk.END)
        self.bmi_label.config(text="")
        self.fat_percentage_label.config(text="")
        self.current_bmi = None
        self.current_fat_percentage = None

    def on_closing(self):
        self.save_data()
        print("Exiting Fitness App")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessApp(root)
    root.mainloop()
