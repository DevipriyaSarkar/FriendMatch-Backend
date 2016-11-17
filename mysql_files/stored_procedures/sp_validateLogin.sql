CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
	IN p_email VARCHAR(45)
)
BEGIN
    SELECT * FROM user WHERE user_email = p_email;
END