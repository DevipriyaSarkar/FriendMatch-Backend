CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateProfile`(
    IN user_id BIGINT,
    IN new_gender CHAR(1),
    IN new_age TINYINT,
    IN new_phone_number VARCHAR(20),
    IN new_location VARCHAr(50),
    IN new_city VARCHAR(20)
)
BEGIN
	DECLARE var_name VARCHAR(45) DEFAULT "user name";
    
    IF ( SELECT NOT EXISTS (SELECT 1 FROM user WHERE user_id = user_id) ) 
    THEN
		SELECT 'Username does not exist !!';
     
    ELSE
		IF ( SELECT NOT EXISTS (SELECT 1 FROM user_details WHERE id = user_id) ) 
        THEN
			SELECT U.user_name INTO var_name FROM user U WHERE U.user_id = user_id;
            INSERT INTO user_details
			(
				id,
                user_name,
				age,
                gender,
                city,
                location,
                phone_number
			)
			VALUES
			(
				user_id,
                var_name,
				new_age,
				new_gender,
                new_city,
                new_location,
                new_phone_number
			);
            
        ELSE
			UPDATE user_details UD
			SET
				UD.age = new_age,
				UD.gender = new_gender,
				UD.city = new_city,
				UD.location = new_location,
				UD.phone_number = new_phone_number
			WHERE UD.id = user_id;
            
		END IF;
    END IF;
END