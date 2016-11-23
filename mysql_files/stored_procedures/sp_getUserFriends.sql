CREATE PROCEDURE `sp_getUserFriends`(
    IN p_user_id BIGINT
)
BEGIN
	SELECT FRIEND.friend_id, USER.user_name, USER.gender 
    FROM user_friend FRIEND, user_details USER
    WHERE FRIEND.id = p_user_id AND
		USER.id = FRIEND.friend_id;
END