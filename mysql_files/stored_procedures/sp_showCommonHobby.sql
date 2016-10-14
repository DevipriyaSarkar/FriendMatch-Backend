CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_showCommonHobby`(
    p_user_id1 INT,
    p_user_id2 INT
)
BEGIN
	SELECT DISTINCT U1.hobby
    FROM user_hobby U1, user_hobby U2
    WHERE U1.id = p_user_id1 AND
		U2.id = p_user_id2 AND
        U1.hobby = U2.hobby;
END