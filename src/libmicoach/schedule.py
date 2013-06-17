from libmicoach import services, workout

class Schedule(object):
    def __init__(self):
        self.workouts = services.CompletedWorkout()

    def getWorkoutList(self):
        log = self.workouts.getWorkoutLog()
        return workout.WorkoutList(log)

    def getLatestWorkout(self):
        w = self.workouts.GetLatestCompletedWorkout()
        return workout.Workout(w)

    def getWorkout(self, id):
        return workout.Workout(self.workouts.GetCompletedWorkoutById(CompletedWorkoutId=id))
