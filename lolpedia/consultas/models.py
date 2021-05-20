from djongo import models

class Season(models.Model):
    year = models.IntegerField()

class League(models.Model):
    name = models.CharField(max_length=280)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

class Split(models.Model):
    name = models.CharField(max_length=280)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

class Round(models.Model):
    name = models.CharField(max_length=280)
    split = models.ForeignKey(Split, on_delete=models.CASCADE)

class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    home = models.CharField(max_length=280)
    visitor = models.CharField(max_length=280)
    result = models.CharField(max_length=280)

class Position(models.Model):
    split = models.ForeignKey(Split, on_delete=models.CASCADE)
    place = models.CharField(max_length=280)
    team = models.CharField(max_length=280)
    wins = models.IntegerField()
    loses = models.IntegerField()