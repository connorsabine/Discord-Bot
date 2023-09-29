from constants import BOT_UID, OPENAI_TOKEN_LIMIT
import openai
import hikari
import lightbulb
import pinecone
from secret import get_secret
from tqdm.auto import tqdm

# PARAMETERS
EMBED_MODEL = "text-embedding-ada-002"
COMPLETION_MODEL = "gpt-3.5-turbo-16k"

# INIT
plugin = lightbulb.Plugin("chatbot")

# OPENAI/PINECONE INIT
openai.organization = get_secret("OPENAI_ORG")
openai.api_key = get_secret("OPENAI_API_KEY")
pinecone.init(api_key=get_secret("PINECONE_API_KEY"), environment=get_secret("PINECONE_ENV"))

# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

# HELPER FUNCTIONS
def get_embed(text):
    return openai.Embedding.create(input=text, engine=EMBED_MODEL)["data"][0]["embedding"]

def get_response(query: str, context: [dict]) -> str:
    context.append(get_message("user", query))
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=context, max_tokens=OPENAI_TOKEN_LIMIT)
    text = response.choices[0].message.content.strip()
    return text

def get_message(role: str, content: str) -> dict:
    return {"role": role, "content": content}

def get_messages(role: str, contents: [str]) -> [dict]:
    context = []
    for content in contents:
        context.append(get_message(role, content))
    return context

def get_index(index: str) -> str:
    return "971040974899929159"
    index = str(index)
    if index not in pinecone.list_indexes():
        # create sample embedding
        embed = get_embed(["Sample document text goes here","there will be several phrases in each batch"])

        # create index
        pinecone.create_index(
            index,
            dimension=len(embed),
            metric='cosine',
            metadata_config={'indexed': ['source', 'id']}
        )

        # log creation of index
        print(f"index {index} created")

    return index

    
def search(index, line, n=3):
    embed = get_embed(line)
    results = pinecone.index_query(index, embed, top_k=n)
    return results

def upsert_vector(index: str, line: str):
    index = pinecone.Index(get_index(index))
    embed = get_embed(line)
    meta = {'text': line}
    index.upsert(vectors=[{
        'id':'vec1', 
        'values':embed, 
        'metadata':meta}])
    
def batch_upsert_vector(index: str, data: [str], batch_size=32):
    index = pinecone.Index(index)
    for i in tqdm(range(0, len(data), batch_size)):
        i_end = min(i+batch_size, len(data))
        lines_batch = data[i: i+batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        res = get_embed(lines_batch)
        embeds = [record['embedding'] for record in res['data']]
        meta = [{'text': line} for line in lines_batch]
        to_upsert = zip(ids_batch, embeds, meta)
        index.upsert(vectors=list(to_upsert))


@plugin.listener(hikari.MessageCreateEvent)
async def message_event(event):

    # add vector to index
    if event.content != None:
        upsert_vector(event.guild_id, event.content)
        print("vector upserted")
    else:
        return

    # respond to message if applicable
    if f"<@{BOT_UID}> " in event.content:
        query = event.content.replace(f"<@{BOT_UID}> ", "")

        index = get_index(event.guild_id)
        context = get_messages("assistant", search(index, query, n=3))

        print("context retrieved")
        print(context)

        await plugin.app.rest.create_message(event.channel_id, get_response(query, context))