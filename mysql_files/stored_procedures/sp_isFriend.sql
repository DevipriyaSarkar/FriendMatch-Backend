CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_isFriend` (
	IN p_user_id1 BIGINT,
    IN p_user_id2 BIGINT
)
BEGIN
	SELECT CASE WHEN EXISTS (
		SELECT UF.id 
		FROM user_friend UF
		WHERE UF.id = p_user_id1 AND
			UF.friend_id = p_user_id2
	)
	THEN 'TRUE'
	ELSE 'FALSE'
	END;
END