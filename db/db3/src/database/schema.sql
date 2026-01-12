DROP VIEW IF EXISTS View_Employee_Details;
DROP VIEW IF EXISTS View_Active_Projects;
DROP TABLE IF EXISTS Project_Assignments;
DROP TABLE IF EXISTS DocumentDepartments; 
DROP TABLE IF EXISTS Documents;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Departments;

CREATE TABLE Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    budget FLOAT DEFAULT 0.0,
    establishment_date DATE
) ENGINE=InnoDB;

CREATE TABLE Projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('planned', 'running', 'finished') DEFAULT 'planned'
) ENGINE=InnoDB;

CREATE TABLE Employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(100),
    salary DECIMAL(10, 2) DEFAULT 0,
    is_manager BOOLEAN DEFAULT FALSE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
) ENGINE=InnoDB;

CREATE TABLE Documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    department_id INT, 
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
) ENGINE=InnoDB;

CREATE TABLE Project_Assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    employee_id INT,
    role VARCHAR(50) DEFAULT 'Member',
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE DocumentDepartments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    department_id INT,
    FOREIGN KEY (document_id) REFERENCES Documents(document_id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE VIEW View_Employee_Details AS
SELECT e.employee_id, e.name, e.position, e.salary, d.name as department_name
FROM Employees e
LEFT JOIN Departments d ON e.department_id = d.department_id;

CREATE VIEW View_Active_Projects AS
SELECT p.name, p.end_date, COUNT(pa.employee_id) as team_size
FROM Projects p
LEFT JOIN Project_Assignments pa ON p.project_id = pa.project_id
WHERE p.status = 'running'
GROUP BY p.project_id;

