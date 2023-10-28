import sys
import time
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QDialog, QFormLayout, QLineEdit, QMessageBox, QTextEdit

# Constants for parking spaces
MAX_BIKES = 100
MAX_CARS = 250
MAX_BICYCLES = 78

class OperationSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Operation")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.operation_label = QLabel("Select an operation:")
        self.operation_input = QComboBox()
        self.operation_input.addItems(["Vehicle Entry", "View Parked Vehicles", "View Available Parking Space", "Generate Bill"])

        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.accept)

        layout.addWidget(self.operation_label)
        layout.addWidget(self.operation_input)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

class ParkingManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.vehicle_data = {
            "Vehicle_Number": [],
            "Vehicle_Type": [],
            "Vehicle_Name": [],
            "Owner_Name": [],
            "Entry_Date": [],
            "Entry_Time": []
        }

        self.load_data()  # Load saved data if available

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Parking Management System")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.operation_selection_dialog = None

        self.operation_selection()

    def operation_selection(self):
        if self.operation_selection_dialog is None:
            self.operation_selection_dialog = OperationSelectionDialog(self)
        if self.operation_selection_dialog.exec_() == QDialog.Accepted:
            selected_operation = self.operation_selection_dialog.operation_input.currentText()
            self.handle_selection(selected_operation)

    def handle_selection(self, selected_option):
        if selected_option == "Vehicle Entry":
            self.vehicle_entry()
        elif selected_option == "View Parked Vehicles":
            self.view_parked_vehicles()
        elif selected_option == "View Available Parking Space":
            self.view_available_space()
        elif selected_option == "Generate Bill":
            self.generate_bill()

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def save_data(self):
        with open('vehicle_data.pkl', 'wb') as f:
            pickle.dump(self.vehicle_data, f)

    def load_data(self):
        try:
            with open('vehicle_data.pkl', 'rb') as f:
                self.vehicle_data = pickle.load(f)
        except FileNotFoundError:
            pass

    def vehicle_entry(self):
        self.clear_layout()
        self.menu_label = QLabel("Vehicle Entry")
        self.layout.addWidget(self.menu_label)
        
        self.vehicle_number_label = QLabel("Vehicle Number:")
        self.vehicle_number_input = QLineEdit()

        self.vehicle_type_label = QLabel("Vehicle Type:")
        self.vehicle_type_input = QComboBox()
        self.vehicle_type_input.addItems(["Bicycle", "Bike", "Car"])

        self.vehicle_name_label = QLabel("Vehicle Name:")
        self.vehicle_name_input = QLineEdit()

        self.owner_name_label = QLabel("Owner Name:")
        self.owner_name_input = QLineEdit()

        self.entry_button = QPushButton("Add Entry")
        self.entry_button.clicked.connect(self.add_entry)

        self.layout.addWidget(self.vehicle_number_label)
        self.layout.addWidget(self.vehicle_number_input)
        self.layout.addWidget(self.vehicle_type_label)
        self.layout.addWidget(self.vehicle_type_input)
        self.layout.addWidget(self.vehicle_name_label)
        self.layout.addWidget(self.vehicle_name_input)
        self.layout.addWidget(self.owner_name_label)
        self.layout.addWidget(self.owner_name_input)
        self.layout.addWidget(self.entry_button)

    def add_entry(self):
        vehicle_number = self.vehicle_number_input.text()
        vehicle_type = self.vehicle_type_input.currentText()
        vehicle_name = self.vehicle_name_input.text()
        owner_name = self.owner_name_input.text()

        if len(vehicle_number) == 12 and vehicle_number not in self.vehicle_data["Vehicle_Number"]:
            self.vehicle_data["Vehicle_Number"].append(vehicle_number)
            self.vehicle_data["Vehicle_Type"].append(vehicle_type)
            self.vehicle_data["Vehicle_Name"].append(vehicle_name)
            self.vehicle_data["Owner_Name"].append(owner_name)
            self.vehicle_data["Entry_Date"].append(time.strftime("%d-%m-%Y"))
            self.vehicle_data["Entry_Time"].append(time.strftime("%H:%M:%S"))

            self.update_parking_space(vehicle_type)

            QMessageBox.information(self, "Success", "Vehicle entry recorded successfully.")
            self.clear_layout()
            self.operation_selection()  # Prompt for another operation
            self.save_data()  # Save the data
        else:
            QMessageBox.warning(self, "Error", "Invalid vehicle number or already exists.")

    def update_parking_space(self, vehicle_type):
        if vehicle_type == 'Bicycle':
            global MAX_BICYCLES
            MAX_BICYCLES -= 1
        elif vehicle_type == 'Bike':
            global MAX_BIKES
            MAX_BIKES -= 1
        elif vehicle_type == 'Car':
            global MAX_CARS
            MAX_CARS -= 1

    def view_parked_vehicles(self):
        self.clear_layout()
        self.menu_label = QLabel("View Parked Vehicles")
        self.layout.addWidget(self.menu_label)
        
        self.parked_vehicles_text = QTextEdit()
        parked_text = "Parked Vehicles:\n"
        for i in range(len(self.vehicle_data["Vehicle_Number"])):
            parked_text += f"{i+1}. Vehicle Number: {self.vehicle_data['Vehicle_Number'][i]}\n"
            parked_text += f"   Vehicle Type: {self.vehicle_data['Vehicle_Type'][i]}\n"
            parked_text += f"   Vehicle Name: {self.vehicle_data['Vehicle_Name'][i]}\n"
            parked_text += f"   Owner Name: {self.vehicle_data['Owner_Name'][i]}\n"
            parked_text += f"   Entry Date: {self.vehicle_data['Entry_Date'][i]}\n"
            parked_text += f"   Entry Time: {self.vehicle_data['Entry_Time'][i]}\n\n"
        self.parked_vehicles_text.setPlainText(parked_text)
        self.parked_vehicles_text.setReadOnly(True)
        self.layout.addWidget(self.parked_vehicles_text)

    def view_available_space(self):
        self.clear_layout()
        self.menu_label = QLabel("View Available Parking Space")
        self.layout.addWidget(self.menu_label)
        
        available_space_text = QTextEdit()
        available_text = f"Available Parking Space:\nBicycles: {MAX_BICYCLES}\nBikes: {MAX_BIKES}\nCars: {MAX_CARS}\n"
        available_space_text.setPlainText(available_text)
        available_space_text.setReadOnly(True)
        self.layout.addWidget(available_space_text)

    def generate_bill(self):
        self.clear_layout()
        self.menu_label = QLabel("Generate Bill")
        self.layout.addWidget(self.menu_label)
        
        self.bill_vehicle_number_label = QLabel("Enter Vehicle Number:")
        self.bill_vehicle_number_input = QLineEdit()

        self.generate_bill_button = QPushButton("Generate Bill")
        self.generate_bill_button.clicked.connect(self.perform_generate_bill)

        self.layout.addWidget(self.bill_vehicle_number_label)
        self.layout.addWidget(self.bill_vehicle_number_input)
        self.layout.addWidget(self.generate_bill_button)

    def perform_generate_bill(self):
        vehicle_number = self.bill_vehicle_number_input.text()
        if vehicle_number in self.vehicle_data["Vehicle_Number"]:
            index = self.vehicle_data["Vehicle_Number"].index(vehicle_number)
            vehicle_type = self.vehicle_data["Vehicle_Type"][index]
            bill_amount = self.calculate_bill(vehicle_type)
            QMessageBox.information(self, "Bill", f"Bill Amount for {vehicle_number}: ${bill_amount:.2f}")
        else:
            QMessageBox.warning(self, "Error", "Vehicle number not found.")

        self.clear_layout()
        self.operation_selection()  # Prompt for another operation

    def calculate_bill(self, vehicle_type):
        if vehicle_type == "Bicycle":
            return 0
        elif vehicle_type == "Bike":
            return 5
        elif vehicle_type == "Car":
            return 10

def main():
    app = QApplication(sys.argv)
    window = ParkingManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
