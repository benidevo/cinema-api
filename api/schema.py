from turtle import title
import graphene
from graphene_django.types import DjangoObjectType
from api.models import Movie, Director

class MovieType(DjangoObjectType):

  class Meta:
    model = Movie
  
  movie_age = graphene.String()

  def resolve_movie_age(self, info):
    return "OOld Movie" if self.year < 2000 else "New Movie"
  

class DirectorType(DjangoObjectType):

  class Meta:
    model = Director


class Query(graphene.ObjectType):
  all_movies = graphene.List(MovieType)
  all_directors = graphene.List(DirectorType)
  director = graphene.Field(DirectorType, id=graphene.String(), first_name=graphene.String(), last_name=graphene.String())
  movie = graphene.Field(MovieType, id=graphene.String(), title=graphene.String())

  def resolve_all_movies(self, info, **kwargs):
    '''
    Retrieve all movies
    '''
    return Movie.objects.all()

  def resolve_movie(self, info, **kwargs):

    id = kwargs.get('id')
    title = kwargs.get('title')

    if id is not None:
      return Movie.objects.get(pk=id)
    
    if title is not None:
      return Movie.objects.get(title=title)
   
    return None

  def resolve_all_directors(self, info, **kwargs):
    return Director.objects.all()

  def resolve_director(self, info, **kwargs):

    id = kwargs.get('id')
    first_name = kwargs.get('first_name')
    last_name = kwargs.get('first_name')

    if id is not None:
      return Director.objects.get(pk=id)

    if first_name is not None:
      return Director.object.ggt(first_name=first_name)

    if last_name is not None:
      return Director.object.ggt(last_name=last_name)
    
    return None

class MovieCreateMutation(graphene.Mutation):
  class Arguments:
    title = graphene.String(required=True)
    year = graphene.Int(required=True)
  
  movie = graphene.Field(MovieType)

  def mutate(self, info, title, year):
    movie = Movie.objects.create(title=title, year=year)

    return MovieCreateMutation(movie=movie)


class MovieUpdateMutation(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)
    title = graphene.String()
    year = graphene.Int()
  
  movie = graphene.Field(MovieType)

  def mutate(self, info, id, title, year):
    try: 
      movie = Movie.objects.get(pk=id)
    except:
      return None

    if title is not None:
      movie.title = title

    if year is not None:
      movie.year = year
    
    movie.save()

    return MovieUpdateMutation(movie=movie)  

class MovieDeleteMutation(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)

  movie = graphene.Field(MovieType)

  def mutate(self, info, id):
    try:
      movie = Movie.objects.get(pk=id)
    except:
      return None

    if movie is not None:
      movie.delete()

    return MovieDeleteMutation(movie=None)

class Mutation:
  create_movie = MovieCreateMutation.Field()
  update_movie = MovieUpdateMutation.Field()
  delete_movie = MovieDeleteMutation.Field()
  