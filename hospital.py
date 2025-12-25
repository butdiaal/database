-- Создание базы данных
CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Таблица пользователей
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role ENUM('admin', 'patient') NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица пациентов
CREATE TABLE patients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    birth_date DATE,
    address TEXT,
    insurance_number VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Таблица врачей
CREATE TABLE doctors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    room_number VARCHAR(20)
);

-- Таблица расписания
CREATE TABLE schedule (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Таблица записей на прием
CREATE TABLE appointments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    appointment_type ENUM('первичный', 'повторный', 'профилактический') DEFAULT 'первичный',
    status ENUM('scheduled', 'completed', 'cancelled') DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Таблица медицинских карт
CREATE TABLE medical_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    visit_date DATE NOT NULL,
    diagnosis TEXT,
    treatment TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Таблица направлений
CREATE TABLE directions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    issue_date DATE NOT NULL,
    reason TEXT NOT NULL,
    specialization VARCHAR(100),
    urgency ENUM('Плановая', 'Срочная', 'Неотложная') DEFAULT 'Плановая',
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Таблица счетов
CREATE TABLE invoices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    payment_method ENUM('наличные', 'карта') DEFAULT 'наличные',
    status ENUM('pending', 'paid') DEFAULT 'pending',
    description TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Вставка тестовых данных
INSERT INTO users (username, password, role, full_name, email, phone) VALUES
('admin', 'admin123', 'admin', 'Администратор Системы', 'admin@hospital.com', '+79990001122'),
('patient1', 'patient123', 'patient', 'Иванов Иван Иванович', 'ivanov@mail.com', '+79991112233'),
('patient2', 'patient456', 'patient', 'Петрова Мария Сергеевна', 'petrova@mail.com', '+79992223344');

INSERT INTO patients (user_id, birth_date, address, insurance_number) VALUES
(2, '1985-05-15', 'ул. Ленина, д.10, кв.5', 'INS123456'),
(3, '1990-08-22', 'ул. Мира, д.25, кв.12', 'INS789012');

INSERT INTO doctors (full_name, specialization, room_number) VALUES
('Смирнов Алексей Владимирович', 'Терапевт', '101'),
('Козлова Елена Петровна', 'Кардиолог', '205'),
('Николаев Дмитрий Сергеевич', 'Невролог', '308'),
('Васильева Ольга Игоревна', 'Хирург', '412'),
('Федоров Сергей Михайлович', 'Офтальмолог', '305');

INSERT INTO schedule (doctor_id, day_of_week, start_time, end_time) VALUES
(1, 'Monday', '09:00:00', '17:00:00'),
(1, 'Wednesday', '09:00:00', '17:00:00'),
(1, 'Friday', '09:00:00', '15:00:00'),
(2, 'Tuesday', '10:00:00', '18:00:00'),
(2, 'Thursday', '10:00:00', '18:00:00'),
(3, 'Monday', '08:00:00', '16:00:00'),
(3, 'Wednesday', '08:00:00', '16:00:00'),
(4, 'Tuesday', '09:00:00', '17:00:00'),
(4, 'Thursday', '09:00:00', '17:00:00'),
(5, 'Friday', '10:00:00', '18:00:00');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, appointment_type, status) VALUES
(1, 1, '2024-01-15', '10:00:00', 'первичный', 'scheduled'),
(2, 2, '2024-01-16', '11:00:00', 'повторный', 'scheduled'),
(1, 3, '2024-01-17', '14:00:00', 'профилактический', 'completed');

INSERT INTO medical_records (patient_id, doctor_id, visit_date, diagnosis, treatment, notes) VALUES
(1, 1, '2024-01-10', 'ОРВИ', 'Постельный режим, обильное питье', 'Температура 37.5'),
(2, 2, '2024-01-12', 'Гипертония', 'Прием лекарств, контроль давления', 'Давление 140/90');

INSERT INTO directions (patient_id, doctor_id, issue_date, reason, specialization, urgency) VALUES
(1, 1, '2024-01-10', 'Общий анализ крови', 'Лабораторные исследования', 'Плановая'),
(2, 2, '2024-01-12', 'ЭКГ сердца', 'Кардиологические исследования', 'Срочная');

INSERT INTO invoices (patient_id, amount, issue_date, due_date, payment_method, status, description) VALUES
(1, 1500.00, '2024-01-10', '2024-02-10', 'наличные', 'pending', 'Консультация терапевта'),
(2, 2500.00, '2024-01-12', '2024-02-12', 'карта', 'paid', 'Консультация кардиолога');
