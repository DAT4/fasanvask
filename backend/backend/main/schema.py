import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphql_jwt.decorators import login_required, superuser_required
from .models import Resident, WashTime

class ResidentType(DjangoObjectType):
    class Meta:
        model = Resident

class WashTimeType(DjangoObjectType):
    class Meta:
        model = WashTime

class Query(ObjectType):
    resident = graphene.Field(
            ResidentType,
            room_number=graphene.String(),
            #token=graphene.String(required=True) // for arguement tokens
            )
    current_resident = graphene.Field(
            ResidentType,
            #room_number=graphene.String(),
            #token=graphene.String(required=True) // for arguement tokens
            )
    washtime = graphene.Field(
            WashTimeType, id=graphene.Int(),
            #token=graphene.String(required=True)
            )
    residents = graphene.List(
            ResidentType,
            #token=graphene.String(required=True)
            )
    washtimes = graphene.List(
            WashTimeType,
            #token=graphene.String(required=True)
            )

    @login_required
    def resolve_resident(self, info, **kwargs):
        room_number = kwargs.get('room_number')

        if room_number is not None:
            return Resident.objects.get(pk=room_number)

        return None

    @login_required
    def resolve_current_resident(self, info, **kwargs):
        room_number = info.context.user.room_number

        if room_number is not None:
            return Resident.objects.get(pk=room_number)

        return None

    @login_required
    def resolve_washtime(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return WashTime.objects.get(pk=id)

        return None

    @login_required
    def resolve_residents(self, info, **kwargs):
        return Resident.objects.all()

    @login_required
    def resolve_washtimes(self, info, **kwargs):
        return WashTime.objects.all()

class ResidentInput(graphene.InputObjectType):
    room_number = graphene.String()
    first_name  = graphene.String()
    last_name   = graphene.String()
    password    = graphene.String()

class WashTimeInput(graphene.InputObjectType):
    id = graphene.ID()
    start_time = graphene.types.datetime.DateTime()
    end_time = graphene.types.datetime.DateTime()
    resident = graphene.Field(ResidentInput)

class CreateResident(graphene.Mutation):
    class Arguments:
        input = ResidentInput(required=True)

    ok = graphene.Boolean()
    resident = graphene.Field(ResidentType)
    
    @staticmethod
    @superuser_required
    def mutate(root, info, input=None):
        ok = True
        resident_instance = Resident(
                first_name=input.first_name,
                last_name=input.last_name,
                room_number=input.room_number,
                password=input.password,
                )
        resident_instance.save()
        return CreateResident(ok=ok, resident=resident_instance)

class ChangeResidentPassword(graphene.Mutation):
    class Arguments:
        room_number = graphene.String(required=True)
        input = ResidentInput(required=True)

    ok = graphene.Boolean()
    resident = graphene.Field(ResidentType)
    
    @login_required
    @staticmethod
    def mutate(root, info, room_number, input=None):
        ok = False
        resident_instance = Resident.objects.get(pk=room_number)
        if resident_instance:
            ok = True
            resident_instance.password=input.password
            resident_instance.save()
            return UpdateResident(ok=ok, resident=resident_instance)
        return UpdateResident(ok=ok, resident=None)

class UpdateResident(graphene.Mutation):
    class Arguments:
        room_number = graphene.String(required=True)
        input = ResidentInput(required=True)

    ok = graphene.Boolean()
    resident = graphene.Field(ResidentType)
    
    @staticmethod
    def mutate(root, info, room_number, input=None):
        ok = False
        resident_instance = Resident.objects.get(pk=room_number)
        if resident_instance:
            ok = True
            resident_instance.first_name=input.first_name
            resident_instance.last_name=input.last_name
            resident_instance.save()
            return UpdateResident(ok=ok, resident=resident_instance)
        return UpdateResident(ok=ok, resident=None)

    
class CreateWashTime(graphene.Mutation):
    class Arguments:
        room_number = graphene.String(required=True)
        input = WashTimeInput(required=True)

    ok = graphene.Boolean()
    washtime = graphene.Field(WashTimeType)
    
    @staticmethod
    def mutate(root, info, room_number, input=None):
        ok = True
        resident_instance = Resident.objects.get(pk=room_number)

        if resident_instance is None:
            return CreateWashTime(ok=False, washtime=None)

        washtime_instance = WashTime(
                start_time=input.start_time,
                end_time=input.end_time,
                resident=resident_instance
                )

        washtime_instance.save()
        return CreateWashTime(ok=ok, washtime=washtime_instance)

class UpdateWashTime(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = WashTimeInput(required=True)

    ok = graphene.Boolean()
    washtime = graphene.Field(WashTimeType)
    
    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        washtime_instance = WashTime.objects.get(pk=id)
        if washtime_instance:
            ok = True
            resident = Resident.objects.get(pk=input.resident_input.id)

            if resident is None:
                return UpdateWashTime(ok=False, washtime=None)

            washtime_instance.start_time=input.start_time
            washtime_instance.end_time=input.end_time
            resident_instance.save()
            washtime_instance.resident.set(resident)

            return UpdateWashTime(ok=ok, washtime=washtime_instance)
        return UpdateWashTime(ok=ok, washtime=None)

class Mutation(graphene.ObjectType):
    create_resident = CreateResident.Field()
    update_resident = UpdateResident.Field()
    create_washtime = CreateWashTime.Field()
    update_washtime = UpdateWashTime.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

