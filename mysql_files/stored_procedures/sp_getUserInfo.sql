CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getUserInfo`(
    IN p_user_id BIGINT
)
BEGIN
	SELECT UD.id, UD.user_name, U.user_email, UD.age, UD.gender, UD.city, UD.location, UD.phone_number
    FROM user_details UD, user U
    WHERE 	U.user_id = UD.id AND
			UD.id = p_user_id;

END