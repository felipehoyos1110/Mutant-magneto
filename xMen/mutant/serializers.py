from rest_framework import serializers


class RegisterDnaSerializer(serializers.Serializer):
    dna = serializers.ListField(
        child=serializers.CharField()
    )


class AllRegisterDnaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    dna = serializers.CharField()
    isMutant = serializers.BooleanField()


class Stats(object):
    def __init__(self, count_mutant_dna, count_human_dna, ratio):
        self.count_mutant_dna = count_mutant_dna
        self.count_human_dna = count_human_dna
        self.ratio = ratio


class StatsSerializer(serializers.Serializer):
    count_mutant_dna = serializers.IntegerField()
    count_human_dna = serializers.IntegerField()
    ratio = serializers.DecimalField(max_digits=5, decimal_places=2)

