from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mutant.models import RegisterDna
from mutant.serializers import RegisterDnaSerializer, AllRegisterDnaSerializer
from mutant.serializers import StatsSerializer

from mutant.serializers import Stats


class MutantView(APIView):
    """ API Registro ADN mustantes"""
    serializer_class = RegisterDnaSerializer

    def get(self, request):
        """ Retorna lista de registro de ADN """
        register = RegisterDna.objects.all()
        serializer = AllRegisterDnaSerializer(register, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crea registro ADN"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            dna_string = serializer.validated_data.get('dna')
            # VALIDA LA CADENA ADN
            if not validateDna(dna_string):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            # VALIDA SI ES MUTANTE
            is_mutant = isMutant(dna_string)
            # REALIZA REGISTRO
            register_dna = RegisterDna(dna=dna_string, isMutant=is_mutant)
            register_dna.save()
            if is_mutant:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def validateDna(dna):
    # LA CADENA SOLO PUEDE TENER LOS VALORES PERMITIDOS
    simpDict = {"A", "T", "C", "G"}
    for c in dna:
        for d in c:
            if d not in simpDict:
                return False
    return True


def isMutant(dna):
    def validateNextValue(x, y):
        # Valida que la consulta del siguiente valor si este dentro del arreglo
        if x < 0 or x > len(dna[0]) - 1 or y < 0 or y > len(dna) - 1:
            return ''
        secuencia = dna[x]
        return secuencia[y]

    totalSecuencias = 0
    # Empieza a recorrer el arreglo
    for row in range(0, len(dna)):
        index = 0
        # Recorre letra por letra
        for col in dna[row]:
            totalHorizontal = 1
            totalVertical = 1
            totalOblicuaIzq = 1
            totalOblicuaDer = 1
            value = col

            # VALIDA CUANTAS REPETICIONES TIENE LA LETRA ACTUAL
            for v in range(1, 4):
                """Validar horizontal misma fila, siguiente columna"""
                if value == validateNextValue(row, index + v):
                    totalHorizontal += 1
                else:
                    totalHorizontal = 0

                """Validar vertical siguiente fila, misma columna"""
                if value == validateNextValue(row + v, index):
                    totalVertical += 1
                else:
                    totalVertical = 0

                """Validar oblicua izquierda siguiente fila, anterior columna"""
                if value == validateNextValue(row + v, index - v):
                    totalOblicuaIzq += 1
                else:
                    totalOblicuaIzq = 0

                """Validar oblicua derecha siguiente fila, siguiente columna"""
                if value == validateNextValue(row + v, index + v):
                    totalOblicuaDer += 1
                else:
                    totalOblicuaDer = 0

            if totalHorizontal >= 4:
                totalSecuencias += 1
            if totalVertical >= 4:
                totalSecuencias += 1
            if totalOblicuaDer >= 4:
                totalSecuencias += 1
            if totalOblicuaIzq >= 4:
                totalSecuencias += 1

            index += 1

    print('                  ****totalSecuencias: ' + str(totalSecuencias))
    if totalSecuencias > 1:
        return True
    else:
        return False


class StatsView(APIView):
    """ API Estadisticas mutantes"""
    serializer_class = StatsSerializer

    def get(self, request):
        """ Retorna estadisticas de registro de ADN """
        mutants = RegisterDna.objects.filter(isMutant=True).count()
        no_mutants = RegisterDna.objects.filter(isMutant=False).count()
        if no_mutants > 0:
            ratio = mutants / no_mutants
        else:
            ratio = 0
        obj = Stats(mutants, no_mutants, ratio)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
