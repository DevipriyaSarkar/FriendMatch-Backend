CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getUserInfo`(
    p_user_id INT
)
BEGIN
	SELECT id, user_name, age, gender, city, location, phone_number
    FROM user_details WHERE id = p_user_id;

END