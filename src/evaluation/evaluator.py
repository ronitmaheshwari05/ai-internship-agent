from src.evaluation.metrics import (
    format_accuracy_score,
    skill_match_score,
    location_relevance_score,
    diversity_score,
    response_count_score
)

#Main Evaluation function
def evaluate_response(skills, location, output):

    #individual scores
   
    format_score = format_accuracy_score(output)
    skill_score = skill_match_score(skills, output)
    location_score = location_relevance_score(location, output)
    diversity = diversity_score(output)
    response_count = response_count_score(output)

   # Weighted Overall Score

    overall_score = round(

        (

            format_score * 0.25 +
            skill_score * 0.30 +
            location_score * 0.15 +
            diversity * 0.20 +
            response_count * 0.10
   ),
2
)

    #Return full report
    return {
        "overall_score" : overall_score,
        "format_accuracy" : format_score,
        "skill_match" : skill_score,
        "location_match" : location_score,
        "diversity_score" : diversity,
        "response_count" : response_count
    }

# Pretty Print Evaluation Report
def print_evaluation(skills, location, output):

    report = evaluate_response(skills, location, output)
    print("\n--- Internship Recommendation Evaluation ---")
    print(f"Overall Score     : {report['overall_score']}")
    print(f"Format Accuracy   : {report['format_accuracy']}")
    print(f"Skill Match       : {report['skill_match']}")
    print(f"Location Match    : {report['location_match']}")
    print(f"Diversity Score   : {report['diversity_score']}")
    print(f"Response Count    : {report['response_count']}")
    print("-------------------------------------------")