from graphene_django import DjangoObjectType
import graphene

from .models import *


class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator

        fields = ("name",
                  "start_date",
                  "end_date",
                  "data_size",
                  "use_case_name",
                  "time_series_type",
                  "sink_name",
                  "process_id",
                  "status",
                  "metadata")


class SeasonalityType(DjangoObjectType):
    class Meta:
        model = SeasonalityComponentDetails

        fields = ("amplitude",
                  "phase_shift",
                  "frequency_type",
                  "frequency_multiplier")


class ConfigurationType(DjangoObjectType):
    class Meta:
        model = Configuration

        fields = ("frequency",
                  "noise_level",
                  "trend_coefficients",
                  "missing_percentage",
                  "outlier_percentage",
                  "cycle_component_amplitude",
                  "cycle_component_frequency",
                  "generator_id",
                  "attribute_id")


class Query(graphene.ObjectType):
    simulators = graphene.List(SimulatorType)
    configs = graphene.List(ConfigurationType)
    seasons = graphene.List(SeasonalityType)

    def resolve_simulators(root, info):
        return Simulator.objects.all()

    def resolve_configs(root, info):
        return Configuration.objects.all()

    def resolve_seasons(root, info):
        return SeasonalityComponentDetails.objects.all()


class SimulatorMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        use_case_name = graphene.String(required=True)

    simulator = graphene.Field(SimulatorType)

    @classmethod
    def mutate(cls, root, info, name, use_case_name):
        simulator = Simulator.objects.get(use_case_name=use_case_name)
        simulator.name = name
        simulator.save()

        return SimulatorMutation(simulator=simulator)


class ConfigurationMutation(graphene.Mutation):
    class Arguments:
        noise_level = graphene.Int(required=True)
        generator_id = graphene.String(required=True)

    configuration = graphene.Field(ConfigurationType)

    @classmethod
    def mutate(cls, root, info, noise_level, generator_id):
        configuration = Configuration.objects.get(generator_id=generator_id)
        configuration.noise_level = noise_level
        configuration.save()

        return ConfigurationMutation(configuration=configuration)


class SeasonalityMutation(graphene.Mutation):
    class Arguments:
        amplitude = graphene.Int(required=True)
        phase_shift = graphene.Float(required=True)

    season = graphene.Field(SeasonalityType)

    @classmethod
    def mutate(cls, root, info, amplitude, phase_shift):
        seasonality = SeasonalityComponentDetails.objects.get(phase_shift=phase_shift)
        seasonality.amplitude = amplitude
        seasonality.save()

        return SeasonalityMutation(season=seasonality)


class Mutation(graphene.ObjectType):
    update_simulator = SimulatorMutation.Field()
    update_configuration = ConfigurationMutation.Field()
    update_seasonality = SeasonalityMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
