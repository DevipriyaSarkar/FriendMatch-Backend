CREATE PROCEDURE `sp_isFriend` (
	p_user_id1 INT,
    p_user_id2 INT
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