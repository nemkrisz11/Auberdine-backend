# Routes

| method | parameters  | return obj | desc | dev |
| ---- | ---- | ---- | ---- | ---- |
| POST /user/register | [name,email,password] | [namevalid: bool, emailvalid: bool, passwordvalid: bool] |  | Németh Krisztián |
| POST /user/login | [name, password] | | JWT returned in Auth header | Németh Krisztián |
| POST /user/logout | - | [success: bool] | | Németh Krisztián |
| GET /user/recommendations | [count: Int]| [recommendations: Place[] ] | Get list of recommendations | Tremmel Márton |
| GET /place/{place_id} | - | [PlaceDetails] | | Tremmel Márton |
| POST /place/rate/ | [place_id: String, rating: integer, description: String] | [success: bool] | | Tremmel Márton |
| GET /user/{user_id} | - | [username, places: Place[]] | All places the user has rated. friend_ratings property contains user rating | Németh Krisztián |
| GET /user/properties/ | - | [user: UserProperties] |  | Németh Krisztián |
| POST /user/properties/ | [name (opt), password] | [namevalid: bool (opt), passwordvalid: bool] | change name and password | Németh Krisztián |
| GET /user/friends/ | - | [friends: User[]] | get friends of the user | Borsodi Regő |
| DELETE /user/friends/ | [friend_id: String] | [deleted: bool] | | Borsodi Regő |
| GET /user/friend_requests/ | - | [friend_requests: User[]] | | Borsodi Regő |
| POST /user/friend_requests/ | [user_id: String, accepted: bool] | [success: bool] | | Borsodi Regő |
| GET /user/search/ | [query: String] | [users: User[]] | | Borsodi Regő |
| POST /user/friend_request/ | [user_id: String] | [success: bool] | | Borsodi Regő |



# Schemas

## UserProperties

| property | type | desc |
| ---- | ---- | ---- |
| name | String	| user name |
| email | String | user email |

## User
| property | type | desc |
| ---- | ---- | ---- |
| user_id | String | user id |
| name | String	| user name |


## Place

| property | type | desc |
| ---- | ---- | ---- |
| place_id | String | |
| name | String | displayed name of the place |
| picture | String | URL of picture |
| rating | Double | |
| friend_ratings | [Rating] | at most three friend ratings of the place|

## PlaceDetails

| property | type | desc |
| ---- | ---- | ---- |
| name | String | displayed name of the place |
| pictures | String[] | array of picture URLs |
| address | String | |
| website | String | |
| location | [Double, Double] | latitude and longitude of the location |
| rating | Double | |
| friend_ratings | [RatingDetails] | 


## Rating
| property | type | desc |
| ---- | ---- | ---- |
| rating | Int | |
| name | String | |


## RatingDetails
| property | type | desc |
| ---- | ---- | ---- |
| user_id | String | user id in database |
| rating | Int | |
| name | String | |
| description | String |  |

# Authorization

- JWT header: ["alg": "HS256", "typ": "JWT"]
- JWT payload properties: [user_id, timestamp]
- If not authorized, return 401