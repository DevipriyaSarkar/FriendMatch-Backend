CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_showCommonHobby`(
    IN p_user_id1 BIGINT,
    IN p_user_id2 BIGINT
)
BEGIN
	SELECT DISTINCT U1.hobby_id, H.hobby_name
    FROM user_hobby U1, user_hobby U2, hobby H
    WHERE U1.id = p_user_id1 AND
		U2.id = p_user_id2 AND
        U1.hobby_id = U2.hobby_id AND
		U1.hobby_id = H.hobby_id;
END