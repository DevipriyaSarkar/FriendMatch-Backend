CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getUserHobby`(
    IN p_user_id BIGINT
)
BEGIN
	SELECT DISTINCT UH.hobby_id, H.hobby_name 
    FROM user_hobby UH, hobby H 
    WHERE UH.id = p_user_id AND
		UH.hobby_id = H.hobby_id;

END