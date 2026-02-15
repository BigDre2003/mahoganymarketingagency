-- database: ../equipment.db
-- SQLite

--DROP TABLE request;

UPDATE equipment SET quantity = 5 WHERE name = 'CNC Milling Machine';

CREATE TABLE IF NOT EXISTS request (
            request_id INTEGER UNIQUE NOT NULL PRIMARY KEY,
            equipment_requested TEXT NOT NULL,
            new_equipment_requested TEXT NOT NULL,
            user TEXT NOT NULL,
            request_status TEXT DEFAULT('pending'),
            request_at TEXT DEFAULT (datetime('now', 'localtime')),
            arrive_at TEXT DEFAULT (datetime('now', 'localtime'))
            
            
            
);

INSERT INTO second_warehouse (name, quantity) VALUES ('3D Printer', '5'), ('Laser Cutter', '5'), ('CNC Milling Machine', '5'),
('Forklift', '5'), ('Welding Machine', '5');

--DELETE FROM users WHERE username = 'IMualis2134';

CREATE TRIGGER IF NOT EXISTS update_request_updated_at
AFTER UPDATE ON request
FOR EACH ROW
BEGIN
    UPDATE request
    SET arrive_at = datetime('now', 'localtime')
    WHERE request_id = OLD.request_id;
END;

--ALTER TABLE equipment DROP COLUMN equipment_status;
                

                 
