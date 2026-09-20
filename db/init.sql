CREATE TABLE usage_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(100)  NOT NULL,
  team      VARCHAR(100)  NOT NULL,
  tool      VARCHAR(50)   NOT NULL,
  tokens    INT           NOT NULL,
  cost      DECIMAL(10,2) NOT NULL,
  used_on   DATE          NOT NULL,
  INDEX idx_team_date (team, used_on)
);
