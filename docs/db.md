# DB docs


## Users

| Field | Type | Notes |
| ---- | :----: | ---- |
| id | ObjectId | | 
| name | String | user name |
| email | String | user email |
| pwd_hash | Binary | password hash  |
| friends | [ObjectId] | list of the user's friends |
| friend_requests | [ObjectId] | list of user ids who sent friend requests to this user |
| preferences | [String] | |
## Places

| Field | Type | Notes |
| ---- | :----: | ---- |
| id | ObjectId | |
| google_place_id | String | id of the place in google places API |
| last_sync | Timestamp | last time sync-ed from places API | 
| name | String | displayed name of the place |
| address | String | |
| location | GeoPoint (2dsphere) | latitude and longitude of the location |
| website | String | URL for the website | 

## Reviews

| Field | Type | Notes |
| ---- | :----: | ---- |
| id | ObjectId | |
| user_id | ObjectId | id of the user posting the review |
| place_id | ObjectId | id of the place reviewed | 
| rating | Integer [1,5] | |
| text | String | review text |

