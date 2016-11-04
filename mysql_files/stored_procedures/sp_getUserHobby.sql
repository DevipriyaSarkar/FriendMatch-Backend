CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getUserHobby`(
    p_user_id INT
)
BEGIN
	SELECT DISTINCT hobby
    FROM user_hobby WHERE id = p_user_id;

END