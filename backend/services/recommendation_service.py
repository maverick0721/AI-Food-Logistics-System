def recommend(user_id, restaurant_id):

    from ml_models.recommendation.predict import predict

    score = predict(user_id, restaurant_id)

    return {

        "user_id": user_id,
        "restaurant_id": restaurant_id,
        "score": score

    }