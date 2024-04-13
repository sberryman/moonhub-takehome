import hashlib
import json
from enum import Enum
from typing import Sequence, Set

import qdrant_client
from llama_index.core import (
    Document,
    Settings,
    StorageContext,
)
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
from llama_index.vector_stores.qdrant import QdrantVectorStore
from neo4j import Driver, GraphDatabase
from nltk.tokenize import word_tokenize
from pydantic import BaseModel, Field
from slugify import slugify
from tqdm import tqdm

# the source data is from
# https://nubela.co/blog/sample-data-for-linkdb/

client = qdrant_client.QdrantClient("http://qdrant:6333")

Settings.embed_model = TextEmbeddingsInference(
    model_name="BAAI/bge-large-en-v1.5",  # required for formatting inference text,
    timeout=60,  # timeout in seconds
    embed_batch_size=10,  # batch size for embedding
    base_url="http://192.168.6.2",
    query_instruction="为这个句子生成表示以用于检索相关文章：",
)
Settings.chunk_size = 500
Settings.chunk_overlap = 16

vector_store = QdrantVectorStore(client=client, collection_name="people")
storage_context = StorageContext.from_defaults(vector_store=vector_store)


class SkillSourceEnum(str, Enum):
    mentioned = "mentioned"
    inferred = "inferred"


class Skill(BaseModel):
    name: str = Field(
        description="Name of the skill. Do not include anything other than computer technology related skills.",
        examples=[
            "Python",
            "Java",
            "C++",
            "Django",
            "Flask",
            "Spring",
            "Postgres",
            "MySQL",
            "MongoDB",
            "Docker",
            "Kubernetes",
            "Jenkins",
            "Agile",
            "Scrum",
            "Kanban",
        ],
    )

    # source: SkillSourceEnum = Field(
    #     description="Source of the skill. Was the skill mentioned or inferred?"
    # )

    # reason: str = Field(
    #     description="If the skill was inferred, what was the reason for the inference? For example, the skill was inferred from an existing skill, be sure to include WHY this skill is presumed to be known. If the skill was mentioned, this field should be empty."
    # )


class Candidate(BaseModel):
    skills: list[Skill] = Field(
        description="List of computer software related skills",
    )


# serialize pydantic model into json schema
pydantic_schema = Skill.schema_json()


def hash_string(input_str) -> str:
    # Create a new SHA256 hash object
    hasher = hashlib.sha256()

    # Convert the input string into bytes and update the hash object
    hasher.update(input_str.encode())

    # Get the hexadecimal representation of the hash
    return hasher.hexdigest()


def extract_skills(text: str) -> Set[str]:
    allowed_skills = [
        "3D Modeling",
        "API",
        "ASP.NET",
        "AWS",
        "Active Record",
        "AdonisJS",
        "Agile Methodologies",
        "Ajax",
        "POLARDDB",
        "DocumentDB",
        "DynamoDB",
        "RDS",
        "Android",
        "Angular",
        "Ant Design",
        "Cassandra",
        "Spark",
        "AppleScript",
        "Arduino",
        "Artificial Intelligence",
        "Assembly",
        "Azure",
        "Azure Cosmos DB (API for MongoDB)",
        "Azure Cosmos DB (Core SQL API)",
        "Bash",
        "Beego",
        "Blazor",
        "Blockchain Technology",
        "Bootstrap",
        "Bulma",
        "C",
        "C#",
        "C++",
        "CPP",
        "CSS",
        "CakePHP",
        "Cassandra",
        "Chakra UI",
        "ClickHouse",
        "Cloudera Impala",
        "CodeIgniter",
        "Couchbase Server",
        "Crystal",
        "Cybersecurity",
        "Dart",
        "Data Analysis",
        "DataStax Astra DB",
        "Deno",
        "DevOps",
        "Django",
        "Docker",
        "Dockerfile",
        "Druid",
        "Echo",
        "Elasticsearch",
        "Element Plus",
        "Elm",
        "Emacs Lisp",
        "Erlang",
        "Express.js",
        "F#",
        "Facebook Presto",
        "FastAPI",
        "FeathersJS",
        "Firebase",
        "Firebird",
        "Flask",
        "Flutter",
        "Fortran",
        "Foundation",
        "Frameworx",
        "Game Development",
        "GameMaker Language",
        "Gin",
        "Git",
        "GitHub",
        "Glsl",
        "Go",
        "Golang",
        "Firestore",
        "Google Cloud",
        "GraphQL",
        "Graphic Design",
        "Greenplum",
        "H2 Database",
        "HBase",
        "HDFS",
        "HTML",
        "Hadoop",
        "Haml",
        "Handlebars.js",
        "Harbor",
        "Haskell",
        "Hazelcast",
        "HeadlessUI",
        "Hyperledger",
        "Db2",
        "InfluxDB",
        "Inform7",
        "Information Security",
        "Ionic Framework",
        "Java",
        "JavaScript",
        "JeffersonDB",
        "Julia",
        "Kafka",
        "KairosDB",
        "Kendo UI",
        "Keycloak",
        "Knox",
        "Kohana",
        "Kotlin",
        "Kubernetes",
        "LaTeX",
        "Laravel",
        "Less",
        "LevelDB",
        "LiteSpeed",
        "Lua",
        "LuaJIT",
        "Lumen",
        "MATLAB",
        "Machine Learning",
        "Makefile",
        "Mapbox GL JS",
        "MariaDB",
        "Markdown",
        "Material UI",
        "Materialize CSS",
        "Matplotlib",
        "Memcached",
        "Mermaid",
        "Microsoft SQL Server",
        "MSSQL",
        "MongoDB",
        "Mongoose",
        "MySQL",
        "NGINX",
        "NativeScript",
        "Neo4j",
        "Network Security",
        "NewSQL",
        "Next.js",
        "Nim",
        "Node.js",
        "NumPy",
        "NuoDB",
        "Nuxt.js",
        "OCaml",
        "ORM",
        "Objective-C",
        "OceanBase",
        "Onsen UI",
        "OpenCV",
        "OpenSearch",
        "Opentelemetry",
        "Oracle",
        "OracleDB",
        "PHP",
        "Pandas",
        "Penetration Testing",
        "Percona",
        "Perl",
        "Phabricator",
        "PhoneGap",
        "PlainText",
        "PlanetScale",
        "PostgreSQL",
        "PowerShell",
        "Preact",
        "Prisma",
        "Processing",
        "Prometheus",
        "Protobuf",
        "Proxysql",
        "Puppet",
        "PureBasic",
        "Python",
        "QML",
        "Quest",
        "R",
        "Racket",
        "Radix",
        "Rails",
        "React",
        "React Native",
        "Redis",
        "Redshift",
        "Remix",
        "RethinkDB",
        "Riak",
        "RoachDB",
        "RobotFramework",
        "Rpkg",
        "Ruby",
        "Rust",
        "SQL",
        "SQLite",
        "Sanic",
        "Sapientia",
        "Sass",
        "Scala",
        "Scheme",
        "Scikit-learn",
        "Scrum",
        "ScyllaDB",
        "Selenium",
        "Sencha Touch",
        "Sequelize",
        "Shaders",
        "Shell",
        "Sidekiq",
        "SignalR",
        "Snowflake",
        "Socket.io",
        "SocketCluster",
        "Solidity",
        "Spanner",
        "Spring Boot",
        "Supabase",
        "Svelte",
        "Swift",
        "Sybase",
        "Symfony",
        "Tailwind",
        "Tailwind CSS",
        "Tcl",
        "TensorFlow",
        "Texinfo",
        "Themeross",
        "Thrift",
        "TiDB",
        "TimescaleDB",
        "TinyDB",
        "TokuMX",
        "Traefik",
        "TrueNAS",
        "Twig",
        "TypeDocs",
        "TypeORM",
        "TypeScript",
        "Unity",
        "Unreal Engine",
        "UnrealScript",
        "Upside",
        "VBScript",
        "VHDL",
        "Vala",
        "Vant",
        "Verilog",
        "Vite",
        "Visual Basic .NET",
        "VoltDB",
        "Vue",
        "Vue.js",
        "Vuetify",
        "VMware",
        "WebAssembly",
        "Websockets",
        "Wren",
        "Xamarin",
        "YAML",
        "Yii Framework",
        "ZooKeeper",
        "jQuery",
    ]

    # word tokenize the source
    tokens = word_tokenize(text.lower())

    # find all the skills
    skills = set()
    for skill in allowed_skills:
        if skill.lower() in tokens:
            skills.add(skill)

    return skills


def process_person(client: Driver, line: str):
    documents: Sequence[Document] = []

    try:
        # read the json object
        data = json.loads(line)
        if not data:
            return

        # create a session
        # with client.session(database="memgraph") as session:
        #     tx = session.begin_transaction()

        #     try:
        #         if not is_enough_token(tx, sender_id, num_of_tokens):
        #             print("Not enough tokens in the account balance.")
        #             return
        #         try:
        #             decrease_sender_balance(tx, sender_id, num_of_tokens)
        #             increase_receiver_balance(tx, receiver_id, num_of_tokens)
        #             tx.commit()  # both should be committed or none
        #         except Exception as e:
        #             raise e  # if exception happened roll back both
        #     finally:
        #         tx.close()  # rolls back if not yet committed
        try:
            # start our document
            p_id = data["public_identifier"]
            if p_id.lower().strip() == "none":
                p_id = data["profile_pic_url"]
            else:
                p_id = f"https://www.linkedin.com/in/{p_id}"

            # hash the id
            id = hash_string(p_id)

            # person
            client.execute_query(
                """
                MERGE (p:Person {id: $id})
                    ON CREATE SET p.first_name = $first_name, p.last_name = $last_name,
                        p.full_name = $full_name, p.profile_pic_url = $profile_pic_url,
                        p.occupation = $occupation, p.headline = $headline, p.connections = $connections, p.url = $url
                """,
                id=id,
                first_name=data["first_name"],
                last_name=data["last_name"],
                full_name=data["full_name"],
                profile_pic_url=data["profile_pic_url"],
                occupation=data["occupation"],
                headline=data["headline"],
                url=p_id,
                connections=data["connections"]
                if "connections" in data and isinstance(data["connections"], int)
                else None,
            )

            # a person has a set of skills
            skills = set[str]()

            # add our person to the index
            documents.append(
                Document(
                    doc_id=id,
                    text=f"""
                Name:
                {data['full_name']}

                Occupation:
                {data['occupation']}

                Headline:
                {data['headline']}

                Location:
                {data['city']}, {data['state']}, {data['country']}
                """,
                    metadata={
                        "person_id": id,
                        "kind": "experience",
                    },
                    excluded_embed_metadata_keys=["kind", "person_id"],
                    excluded_llm_metadata_keys=["kind", "person_id"],
                )
            )

            # experience(s)
            if (
                "experiences" in data
                and data["experiences"]
                and len(data["experiences"]) > 0
            ):
                for experience in data["experiences"]:
                    c_id = experience["company_linkedin_profile_url"]
                    if not c_id or c_id.lower().strip() == "none":
                        c_id = experience["company"]

                    # location is used in multiple places
                    location = (
                        experience["location"]
                        if "location" in experience and experience["location"]
                        else "UNKNOWN"
                    )

                    e_id = ":".join(
                        [
                            str(experience["starts_at"]["year"])
                            if "starts_at" in experience and experience["starts_at"]
                            else "",
                            str(experience["starts_at"]["month"])
                            if "starts_at" in experience and experience["starts_at"]
                            else "",
                            str(experience["starts_at"]["day"])
                            if "starts_at" in experience and experience["starts_at"]
                            else "",
                            experience["company"],
                            experience["title"]
                            if "title" in experience and experience["title"]
                            else "",
                        ]
                    )

                    l_id = slugify(location)
                    lp_id = ":".join(
                        [
                            location,
                            experience["company"],
                            p_id,
                        ]
                    )

                    # hash the ids
                    c_id = hash_string(c_id)
                    e_id = hash_string(e_id)
                    l_id = hash_string(l_id)
                    lp_id = hash_string(lp_id)

                    # do we have an end date?
                    has_ends_at = (
                        True
                        if "ends_at" in experience
                        and experience["ends_at"]
                        and "year" in experience["ends_at"]
                        and "month" in experience["ends_at"]
                        and "day" in experience["ends_at"]
                        else False
                    )
                    has_starts_at = (
                        True
                        if "starts_at" in experience
                        and experience["starts_at"]
                        and "year" in experience["starts_at"]
                        and "month" in experience["starts_at"]
                        and "day" in experience["starts_at"]
                        else False
                    )

                    document: list[str] = []
                    document.append(f"\t* Company: {experience['company']}")
                    document.append(f"\t\t* Title: {experience['title']}")
                    if has_starts_at:
                        document.append(
                            f"\t\t* Started: {experience['starts_at']['year']}-{experience['starts_at']['month']}-{experience['starts_at']['day']}"
                        )
                    if has_ends_at:
                        document.append(
                            f"\t\t* Ended: {experience['ends_at']['year']}-{experience['ends_at']['month']}-{experience['ends_at']['day']}"
                        )
                    else:
                        document.append("\t\t* Current / Present Job")

                    if "description" in experience and experience["description"]:
                        document.append(
                            f"\t\t* Description: {experience['description']}"
                        )

                    client.execute_query(
                        f"""
                        MATCH (p:Person {"{id: $p_id}"})

                        MERGE (c:Company {"{id: $c_id}"})
                        ON CREATE SET c.name = $company, c.url = $url, c.logo = $logo

                        MERGE (l:CompanyLocation {"{id: $l_id}"})
                        ON CREATE SET l.name = $location

                        MERGE (p)-[r:WORKS_FOR {"{id: $e_id}"}]->(c)
                        SET r.title = $title, r.description = $description{" , r.end = date({year: $ends_year, month: $ends_month, day: $ends_day})" if has_ends_at else ""}{" , r.start = date({year: $starts_year, month: $starts_month, day: $starts_day})" if has_starts_at else ""}

                        MERGE (p)-[a:WORKS_AT]->(l)
                        SET a.id = $lp_id{", a.end = date({year: $ends_year, month: $ends_month, day: $ends_day})" if has_ends_at else ""}{", a.start = date({year: $starts_year, month: $starts_month, day: $starts_day})" if has_starts_at else ""}

                        MERGE (c)-[:HAS_BRANCH {"{id: $l_id}"}]->(l)
                        """,
                        # person
                        p_id=id,
                        # company
                        c_id=c_id,
                        company=experience["company"].strip(),
                        e_id=e_id,
                        # location
                        l_id=l_id,
                        location=location,
                        lp_id=lp_id,
                        # optionals
                        url=experience["company_linkedin_profile_url"]
                        if "company_linkedin_profile_url" in experience
                        else None,
                        logo=experience["logo_url"]
                        if "logo_url" in experience
                        else None,
                        title=experience["title"]
                        if "title" in experience and experience["title"]
                        else None,
                        description=experience["description"]
                        if "description" in experience and experience["description"]
                        else None,
                        ends_year=experience["ends_at"]["year"]
                        if "ends_at" in experience
                        and experience["ends_at"]
                        and "year" in experience["ends_at"]
                        else None,
                        ends_month=experience["ends_at"]["month"]
                        if "ends_at" in experience
                        and experience["ends_at"]
                        and "month" in experience["ends_at"]
                        else None,
                        ends_day=experience["ends_at"]["day"]
                        if "ends_at" in experience
                        and experience["ends_at"]
                        and "day" in experience["ends_at"]
                        else None,
                        starts_year=experience["starts_at"]["year"]
                        if "starts_at" in experience
                        and experience["starts_at"]
                        and "year" in experience["starts_at"]
                        else None,
                        starts_month=experience["starts_at"]["month"]
                        if "starts_at" in experience
                        and experience["starts_at"]
                        and "month" in experience["starts_at"]
                        else None,
                        starts_day=experience["starts_at"]["day"]
                        if "starts_at" in experience
                        and experience["starts_at"]
                        and "day" in experience["starts_at"]
                        else None,
                    )

                    # add our person to the index
                    documents.append(
                        Document(
                            doc_id=e_id,
                            text="\n".join(document),
                            metadata={
                                "person_id": id,
                                "kind": "experience",
                            },
                            excluded_embed_metadata_keys=["kind", "person_id"],
                            excluded_llm_metadata_keys=["kind", "person_id"],
                        )
                    )

                    # extract skills from the description
                    if "description" in experience and experience["description"]:
                        skills.update(extract_skills(experience["description"]))

            if "languages" in data and data["languages"] and len(data["languages"]) > 0:
                for language in data["languages"]:
                    if not isinstance(language, str):
                        continue

                    # build our id
                    l_id = hash_string(language.strip().lower())

                    client.execute_query(
                        f"""
                        MATCH (p:Person {"{id: $p_id}"})
                        MERGE (l:Language {"{id: $l_id}"})
                        ON CREATE SET l.name = $name

                        MERGE (p)-[r:SPEAKS]->(l)
                        """,
                        p_id=id,
                        l_id=l_id,
                        name=language,
                    )

            # do we care about education?
            # it doesn't really help with searching for candidates (other than degree...)
            if "education" in data and data["education"] and len(data["education"]) > 0:
                for education in data["education"]:
                    s_id = education["school_linkedin_profile_url"]
                    if not s_id or s_id.lower().strip() == "none":
                        s_id = education["school"]

                    se_id = ":".join(
                        [
                            str(education["starts_at"]["year"])
                            if "starts_at" in education and education["starts_at"]
                            else "",
                            str(education["starts_at"]["month"])
                            if "starts_at" in education and education["starts_at"]
                            else "",
                            str(education["starts_at"]["day"])
                            if "starts_at" in education and education["starts_at"]
                            else "",
                            education["school"],
                            education["degree_name"]
                            if "degree_name" in education and education["degree_name"]
                            else "",
                        ]
                    )

                    # hash the ids
                    s_id = hash_string(s_id)
                    se_id = hash_string(se_id)

                    # do we have an end date?
                    has_ends_at = (
                        True
                        if "ends_at" in education
                        and education["ends_at"]
                        and "year" in education["ends_at"]
                        and "month" in education["ends_at"]
                        and "day" in education["ends_at"]
                        else False
                    )
                    has_starts_at = (
                        True
                        if "starts_at" in education
                        and education["starts_at"]
                        and "year" in education["starts_at"]
                        and "month" in education["starts_at"]
                        and "day" in education["starts_at"]
                        else False
                    )

                    client.execute_query(
                        f"""
                        MATCH (p:Person {"{id: $p_id}"})
                        MERGE (s:School {"{id: $s_id}"})
                        ON CREATE SET s.name = $school, s.url = $url, s.logo = $logo

                        MERGE (p)-[r:STUDY_AT {"{id: $se_id}"}]->(s)
                        SET r.degree = $degree_name, r.field = $field_of_study, r.description = $description{" , r.end = date({year: $ends_year, month: $ends_month, day: $ends_day})" if has_ends_at else ""}{" , r.start = date({year: $starts_year, month: $starts_month, day: $starts_day})" if has_starts_at else ""}
                        """,
                        # person
                        p_id=id,
                        # school
                        s_id=s_id,
                        school=education["school"].strip(),
                        # relationship
                        se_id=se_id,
                        # optionals
                        url=education["school_linkedin_profile_url"]
                        if "school_linkedin_profile_url" in education
                        else None,
                        logo=education["logo_url"] if "logo_url" in education else None,
                        degree_name=education["degree_name"]
                        if "degree_name" in education and education["degree_name"]
                        else None,
                        field_of_study=education["field_of_study"]
                        if "field_of_study" in education and education["field_of_study"]
                        else None,
                        description=education["description"]
                        if "description" in education and education["description"]
                        else None,
                        ends_year=education["ends_at"]["year"]
                        if "ends_at" in education
                        and education["ends_at"]
                        and "year" in education["ends_at"]
                        else None,
                        ends_month=education["ends_at"]["month"]
                        if "ends_at" in education
                        and education["ends_at"]
                        and "month" in education["ends_at"]
                        else None,
                        ends_day=education["ends_at"]["day"]
                        if "ends_at" in education
                        and education["ends_at"]
                        and "day" in education["ends_at"]
                        else None,
                        starts_year=education["starts_at"]["year"]
                        if "starts_at" in education
                        and education["starts_at"]
                        and "year" in education["starts_at"]
                        else None,
                        starts_month=education["starts_at"]["month"]
                        if "starts_at" in education
                        and education["starts_at"]
                        and "month" in education["starts_at"]
                        else None,
                        starts_day=education["starts_at"]["day"]
                        if "starts_at" in education
                        and education["starts_at"]
                        and "day" in education["starts_at"]
                        else None,
                    )

            if (
                "accomplishment_projects" in data
                and data["accomplishment_projects"]
                and len(data["accomplishment_projects"]) > 0
            ):
                for project in data["accomplishment_projects"]:
                    if "description" in project and project["description"]:
                        skills.update(extract_skills(project["description"]))

            # if we have skills, add them to the graph
            if len(skills) > 0:
                for skill in skills:
                    client.execute_query(
                        f"""
                        MATCH (p:Person {"{id: $p_id}"})
                        MERGE (s:Skill {"{id: $s_id}"})
                        ON CREATE SET s.name = $name

                        MERGE (p)-[r:HAS_SKILL]->(s)
                        """,
                        p_id=id,
                        s_id=slugify(skill),
                        name=skill,
                    )
        except Exception as e:
            print(f"Memgraph: {e}")
            pass

        # try:
        #     # index our document(s)
        #     if len(documents) > 1:
        #         VectorStoreIndex.from_documents(
        #             documents=documents,
        #             storage_context=storage_context,
        #         )
        # except Exception as e:
        #     print(f"Error indexing: {e}")
        #     return

    except json.JSONDecodeError as e:
        print(f"Error decoding json: {e}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return


def app():
    # print(pydantic_schema)
    # return
    with GraphDatabase.driver("bolt://memgraph-platform:7687", auth=("", "")) as client:
        # open the source file
        source_file = "/workspaces/api/tests/data/us_person_profile.txt"

        # count the number of lines
        with open(source_file) as f_in:
            num_lines = sum(1 for _ in f_in)

        # read the file
        with open(source_file) as f_in:
            # each line is a json object
            for _idx, line in tqdm(enumerate(f_in), total=num_lines):
                process_person(client, line)

                # if idx > 100:
                #     break


if __name__ == "__main__":
    app()
