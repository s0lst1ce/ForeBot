import logging
import discord
import os
from settings import *
from utilities import *

#########################################
#										#
#										#
#			Setting up logging			#
#										#
#										#
#########################################
local_logger = logging.getLogger(__name__)
local_logger.setLevel(LOGGING_LEVEL)
local_logger.addHandler(LOGGING_HANDLER)
local_logger.info("Innitalized {} logger".format(__name__))



#########################################
#										#
#										#
#			Making commands				#
#										#
#										#
#########################################


class Slapping(commands.Cog):
	"""a suite of commands meant to help moderators handle the server"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@is_init()
	@has_auth("manager")
	async def slap(self, ctx, member:discord.Member):
		'''Meant to give a warning to misbehavioring members. Cumulated slaps will result in warnings, role removal and eventually kick. Beware the slaps are loged throughout history and are cross-server'''
		#slapping
		with ConfigFile(ctx.guild.id)[member.id] as slaps:
			slaps +=1
			#warning
			await ctx.send("{} you've been slapped by {} because of your behavior! This is the {} time. Be careful, if you get slapped too much there *will* be consequences !".format(member.mention, ctx.message.author.mention, slaps))

	@commands.command()
	@is_init()
	@has_auth("manager")
	async def pardon(self, ctx, member:discord.Member, nbr=0):
		'''Pardonning a member resets his slaps count.'''

		with ConfigFile(ctx.guild.id)[member.id] as slaps:
			if nbr==0 or slaps<nbr:
				slaps=0
			else:
				slaps -=nbr

			await ctx.send("{} you've been pardonned by {}.\t ({} slaps left)".format(member.mention, ctx.author.mention, slaps))

def setup(bot):
	bot.add_cog(Slapping(bot))