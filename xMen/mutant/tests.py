from django.test import TestCase
from mutant.models import RegisterDna
from rest_framework import status


class MutantViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        RegisterDna.objects.create(dna="['ATGCGA', 'CAGTGC', 'TTATGT', 'AGAAGG', 'CCCCTA', 'TCACTG']", isMutant=True)

    def test_get_register(self):
        response = self.client.get('/mutant/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(RegisterDna.objects.all()))

    def test_create_register_mutant(self):
        """
        Crear un nuevo registro validacion de mutante
        """
        data = {"dna":["ATGCGA",
                       "CAGTGC",
                       "TTATGT",
                       "AGAAGG",
                       "CCCCTA",
                       "TCACTG"]}
        response = self.client.post('/mutant/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_register_no_mutant(self):
        """
        Crear un nuevo registro validacion de mutante
        """
        data = {"dna":["ATGCGA",
                       "CAGTCC",
                       "TTATGT",
                       "AGAAGG",
                       "ACCCTA",
                       "TCACTG"]}
        response = self.client.post('/mutant/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_register_valor_no_valido(self):
        """
        Crear un nuevo registro validacion de mutante, no permitido por valor no valido
        """
        data = {"dna":["ATGCGS",
                       "CAGTGC",
                       "TTATGT",
                       "AGAAGG",
                       "CCCCTA",
                       "TCACTG"]}
        response = self.client.post('/mutant/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_stats(self):
        self.test_create_register_no_mutant()
        self.test_create_register_mutant()
        mutants = RegisterDna.objects.filter(isMutant=True).count()
        no_mutants = RegisterDna.objects.filter(isMutant=False).count()
        response = self.client.get('/stats/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, mutants)
        self.assertEqual(1, no_mutants)
        self.assertEqual(response.data['count_mutant_dna'], mutants)
        self.assertEqual(response.data['count_human_dna'], no_mutants)
