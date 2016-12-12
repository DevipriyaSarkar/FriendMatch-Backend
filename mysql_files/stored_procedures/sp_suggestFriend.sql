CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_suggestFriend`(
    IN p_user_id BIGINT
)
BEGIN
	(SELECT DISTINCT USER.id, USER.user_name, USER.age, USER.gender
    FROM user_details USER, user_hobby HOBBY1
    WHERE USER.id = HOBBY1.id AND
		USER.id <> p_user_id AND
		HOBBY1.hobby_id IN
			(SELECT hobby_id FROM user_hobby WHERE id = p_user_id) AND
		USER.id NOT IN
			(SELECT friend_id FROM user_friend
            WHERE id = p_user_id)
	)
	UNION
    (SELECT DISTINCT USER.id, USER.user_name, USER.age, USER.gender
    FROM user_details USER, user_hobby HOBBY1
    WHERE USER.id = HOBBY1.id AND
		USER.id <> p_user_id AND
		HOBBY1.hobby_id IN
			(
				SELECT related_hobby_id FROM related_hobby
                WHERE hobby_id IN
					(SELECT hobby_id FROM user_hobby WHERE id = p_user_id)
			) AND
		USER.id NOT IN
			(SELECT friend_id FROM user_friend
            WHERE id = p_user_id)
	);
END