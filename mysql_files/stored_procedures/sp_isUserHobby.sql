CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_isUserHobby`(
	IN p_user_id BIGINT,
    IN p_hobby_id BIGINT
)
BEGIN
	SELECT CASE WHEN EXISTS (
		SELECT UH.id
		FROM user_hobby UH
		WHERE UH.id = p_user_id AND
			UH.hobby_id = p_hobby_id
	)
	THEN 'TRUE'
	ELSE 'FALSE'
	END;
END