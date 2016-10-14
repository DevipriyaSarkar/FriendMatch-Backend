CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN new_name VARCHAR(45),
    IN new_username VARCHAR(45),
    IN new_password VARCHAR(100)
)
BEGIN
    IF ( SELECT EXISTS (SELECT 1 FROM user WHERE user_username = new_username) ) THEN
     
        SELECT 'Username Exists !!';
     
    ELSE
     
        INSERT INTO user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            new_name,
            new_username,
            new_password
        );
     
    END IF;
END