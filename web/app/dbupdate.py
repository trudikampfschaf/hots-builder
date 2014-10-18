from app import app
from os import walk 
from models import db
from app import models, db

def update():
	path = '/home/fthomas/Dokumente/hots-builder/web/app/static/hero-data/'
	(_, _, available_heroes) = walk(path).next()
	available_heroes.remove('weekly-heroes')
	available_heroes.sort()
	
	print 'Found heroes:', available_heroes		

	for hero in available_heroes:
		print '\nCurrent hero:', hero
		with open('/home/fthomas/Dokumente/hots-builder/web/app/static/hero-data/' + hero) as file:
			role = file.readline().strip()
			print 'Role:', role
			abilities = []
			for row in file:
				try:
					(ability, text) = row.split(';;')
					(lvl, text) = text.split(';')
				except ValueError:
					print 'Format Error:', row
				abilities.append((ability, lvl, text.strip()))
			
			exist = models.Hero.query.filter_by(name=hero).first()
			if not exist == None:
				print hero, 'exists'
				hero_id = models.Hero.query.filter_by(name=hero).first().id
                                print 'Hero id:', hero_id
				for (ability, lvl, text) in abilities: 
					update_ability(ability, text, lvl, hero_id)
			else: 
				print hero, 'doesnt exist'
				insert_hero(hero, role)
				
				hero_id = models.Hero.query.filter_by(name=hero).first().id
				print 'New id:', hero_id
				
				for (ability, lvl, text) in abilities:
					insert_ability(ability, text, lvl, hero_id)


def insert_build(name, text, hero, build, votes=0, pos_votes=0):
	from time import strftime
	date = strftime("%H:%M:%S - %d/%m/%Y")
	print date
	build = models.Build(name=name, text=text, hero=hero, votes=votes, pos_votes=pos_votes, build=build, date=date)

	from sqlalchemy.exc import IntegrityError
	try:
		db.session.add(build)
		db.session.commit()
		return True

	except IntegrityError:
		print 'IntegrityError: Duplicate name'	
		return False

def get_build(name):
	build = models.Build.query.filter_by(name=name).first()
	return build

def get_best_builds(count):
	builds = models.Build.query.order_by(models.Build.pos_votes.desc()).limit(count)
	builds = builds.all()
	return builds

def get_latest_builds(count):
	builds = models.Build.query.order_by(models.Build.date.desc()).limit(count)
	builds = builds.all()
	return builds

def upvote(name):
	build = models.Build.query.filter_by(name=name).first()
	build.pos_votes = build.pos_votes + 1
	db.session.commit()

def insert_hero(name, role):
	hero = models.Hero(name=name, role=role)
	db.session.add(hero)
	db.session.commit()

def insert_ability(name, text, lvl, hero_id):
	ability = models.Ability(name=name, text=text, lvl=lvl, hero_id=hero_id)
	db.session.add(ability)
	db.session.commit()

def update_ability(name, text, lvl, hero_id):
	ability = models.Ability.query.filter_by(name=name, lvl=lvl, hero_id=hero_id).first()

	if ability == None:
		print 'Inserting:', name, lvl, hero_id
		insert_ability(name, text, lvl, hero_id)
	else:
		ability.text = text
		db.session.commit()

def insert_id(u_agent, ip):
	import hashlib
	hash = hashlib.sha224(u_agent + ip).hexdigest()
	pass

def get_hero_abilities(name, lvl):
	hero_id = models.Hero.query.filter_by(name=name).first().id
	abilities = models.Ability.query.filter_by(hero_id=hero_id, lvl=lvl).all()
	return abilities

def get_build_abilities(name):
	build = models.Build.query.filter_by(name=name).first.build
	return build
	
	
def get_abilityname_by_id(id):
	ability_name = models.Ability.query.filter_by(id=id).first().name
	return ability_name
