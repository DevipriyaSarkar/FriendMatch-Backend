CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getUserFriends`(
    p_user_id INT
)
BEGIN
	SELECT FRIEND.friend_id, USER.user_name
    FROM user_friend FRIEND, user_details USER
    WHERE FRIEND.id = p_user_id AND
		USER.id = FRIEND.friend_id;
END