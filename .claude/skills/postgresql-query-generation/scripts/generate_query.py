#!/usr/bin/env python3
"""
PostgreSQL Query Generation - Domain-Agnostic Script

This script performs automatic domain discovery and generates optimized
PostgreSQL queries for any Entity Framework Core project.

Usage:
    python generate_query.py --query "get all products with category" --project-root "."
    python generate_query.py --interactive
    python generate_query.py --discover-only --output schema.json
"""

import os
import sys
import json
import re
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class EntityProperty:
    """Represents a property of an entity"""
    name: str
    type: str
    is_nullable: bool
    max_length: Optional[int] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    referenced_entity: Optional[str] = None


@dataclass
class EntityInfo:
    """Represents discovered entity information"""
    name: str
    namespace: str
    base_class: Optional[str]
    interfaces: List[str]
    properties: List[EntityProperty]
    table_name: str
    schema: str = "public"
    is_multi_tenant: bool = False
    is_soft_delete: bool = False


@dataclass
class RelationshipInfo:
    """Represents a relationship between entities"""
    source_entity: str
    target_entity: str
    relationship_type: str  # one-to-many, many-to-one, many-to-many
    source_fk: Optional[str] = None
    join_entity: Optional[str] = None
    source_navigation: Optional[str] = None
    target_navigation: Optional[str] = None


class DomainDiscovery:
    """Discovers domain structure from C# entity files"""

    # Patterns for entity detection
    ENTITY_BASE_PATTERNS = [
        r'class\s+\w+.*:\s*.*FullAuditedAggregateRoot',
        r'class\s+\w+.*:\s*.*AuditedAggregateRoot',
        r'class\s+\w+.*:\s*.*AggregateRoot',
        r'class\s+\w+.*:\s*.*SetupEntity',
        r'class\s+\w+.*:\s*.*Entity<',
        r'class\s+\w+.*:\s*.*IAggregateRoot',
        r'class\s+\w+.*:\s*.*IMultiTenant',
        r'class\s+\w+.*:\s*.*ISoftDelete',
    ]

    # Property type mapping to PostgreSQL
    TYPE_MAPPING = {
        'Guid': 'UUID',
        'Guid?': 'UUID',
        'int': 'INTEGER',
        'int?': 'INTEGER',
        'long': 'BIGINT',
        'long?': 'BIGINT',
        'string': 'VARCHAR(256)',
        'bool': 'BOOLEAN',
        'bool?': 'BOOLEAN',
        'DateTime': 'TIMESTAMPTZ',
        'DateTime?': 'TIMESTAMPTZ',
        'decimal': 'NUMERIC',
        'decimal?': 'NUMERIC',
        'double': 'DOUBLE PRECISION',
        'double?': 'DOUBLE PRECISION',
        'float': 'REAL',
        'float?': 'REAL',
        'short': 'SMALLINT',
        'short?': 'SMALLINT',
        'byte': 'SMALLINT',
        'byte?': 'SMALLINT',
        'JObject': 'JSONB',
        'object': 'JSONB',
        'JsonDocument': 'JSONB',
    }

    # Standard fields from ABP base classes
    STANDARD_ABP_FIELDS = {
        'Id': 'Guid',
        'TenantId': 'Guid?',
        'CreationTime': 'DateTime',
        'CreatorId': 'Guid?',
        'LastModificationTime': 'DateTime?',
        'LastModifierId': 'Guid?',
        'IsDeleted': 'bool',
        'DeleterId': 'Guid?',
        'DeletionTime': 'DateTime?',
    }

    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.entities: Dict[str, EntityInfo] = {}
        self.relationships: List[RelationshipInfo] = []
        self.base_classes: Dict[str, List[EntityProperty]] = {}

    def discover(self) -> Dict[str, Any]:
        """Run full domain discovery"""
        print(f"[*] Starting domain discovery in: {self.project_root}")

        # Step 1: Find entity files
        entity_files = self._find_entity_files()
        print(f"   Found {len(entity_files)} potential entity files")

        # Step 2: Parse entities
        for file_path in entity_files:
            self._parse_entity_file(file_path)

        print(f"   Discovered {len(self.entities)} entities")

        # Step 3: Build relationships
        self._build_relationship_graph()
        print(f"   Identified {len(self.relationships)} relationships")

        # Step 4: Build schema model
        schema_model = self._build_schema_model()

        return schema_model

    def _find_entity_files(self) -> List[Path]:
        """Find all C# files containing entity definitions"""
        entity_files = []

        # Common domain entity locations
        search_paths = [
            self.project_root / "src",
            self.project_root / "Domain",
            self.project_root / "application",
            self.project_root / "Applications",
        ]

        for search_path in search_paths:
            if not search_path.exists():
                continue

            # Look for Domain/Entities directories
            for domain_path in search_path.glob("**/Domain/Entities/**/*.cs"):
                if self._is_entity_file(domain_path):
                    entity_files.append(domain_path)

            # Also check for Entities directly
            for entities_path in search_path.glob("**/Entities/**/*.cs"):
                if self._is_entity_file(entities_path):
                    entity_files.append(entities_path)

        return entity_files

    def _is_entity_file(self, file_path: Path) -> bool:
        """Check if file contains entity definition"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(10000)  # Read first 10KB

            # Check for entity patterns
            for pattern in self.ENTITY_BASE_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    return True

            # Check for entity base classes
            if re.search(r'(public|internal)\s+class\s+\w+.*Entity<', content, re.IGNORECASE):
                return True

        except Exception as e:
            pass

        return False

    def _parse_entity_file(self, file_path: Path):
        """Parse entity file to extract entity information"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract namespace
            namespace_match = re.search(r'namespace\s+([^\n{]+)', content)
            namespace = namespace_match.group(1).strip() if namespace_match else ""

            # Find class definition
            class_pattern = r'(public|internal|protected)?\s+(abstract\s+)?class\s+(\w+)\s*[:{\n]'
            class_match = re.search(class_pattern, content, re.IGNORECASE)

            if not class_match:
                return

            class_name = class_match.group(3)

            # Extract base class and interfaces
            class_declaration = class_match.group(0)
            base_class = None
            interfaces = []

            # Extract base class before first comma if any
            if ':' in class_declaration:
                after_colon = class_declaration.split(':', 1)[1]
                parts = [p.strip() for p in after_colon.split(',')]

                for part in parts:
                    if '<' in part:  # Generic base like FullAuditedAggregateRoot<Guid>
                        base_class = part
                    elif part.startswith('I') and not part.startswith('IAggregateRoot'):
                        interfaces.append(part)

            # Determine table name from namespace or class name
            table_name = self._infer_table_name(class_name, namespace)

            # Parse properties (simplified - would need full parser for production)
            properties = self._parse_properties(content, class_name)

            # Detect multi-tenancy and soft delete
            is_multi_tenant = any(p.name == 'TenantId' for p in properties)
            is_soft_delete = any(p.name == 'IsDeleted' for p in properties)

            entity = EntityInfo(
                name=class_name,
                namespace=namespace,
                base_class=base_class,
                interfaces=interfaces,
                properties=properties,
                table_name=table_name,
                schema=self._infer_schema(namespace),
                is_multi_tenant=is_multi_tenant,
                is_soft_delete=is_soft_delete
            )

            self.entities[class_name] = entity
            print(f"   [OK] Parsed: {class_name} ({len(properties)} properties)")

        except Exception as e:
            print(f"   [ERROR] Error parsing {file_path}: {e}")

    def _parse_properties(self, content: str, class_name: str) -> List[EntityProperty]:
        """Parse properties from C# class"""
        properties = []

        # Simplified property parsing
        # Matches: public Guid Id { get; set; }
        property_pattern = r'(public|internal|protected|private)?\s+(virtual\s+)?([^\n{]+?)\s+(\w+)\s*{\s*get\s*;\s*set\s*;\s*}'

        # Also match fields
        field_pattern = r'(public|internal|protected|private)?\s+(virtual\s+)?([^\n{]+?)\s+(\w+)\s*;'

        for pattern in [property_pattern, field_pattern]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                type_str = match.group(3).strip()
                prop_name = match.group(4)

                # Skip certain properties
                if prop_name in ['Id'] and type_str not in ['Guid', 'int', 'long']:
                    continue

                is_nullable = '?' in type_str
                base_type = type_str.replace('?', '').strip()

                # Check for foreign key pattern
                is_foreign_key = False
                referenced_entity = None
                if prop_name.endswith('Id') and prop_name != 'Id':
                    is_foreign_key = True
                    # Extract entity name from {EntityName}Id
                    entity_name = prop_name[:-2]
                    if entity_name in self.entities or any(e.name == entity_name for e in self.entities.values()):
                        referenced_entity = entity_name

                prop = EntityProperty(
                    name=prop_name,
                    type=base_type,
                    is_nullable=is_nullable,
                    is_primary_key=(prop_name == 'Id'),
                    is_foreign_key=is_foreign_key,
                    referenced_entity=referenced_entity
                )

                # Avoid duplicates
                if not any(p.name == prop_name for p in properties):
                    properties.append(prop)

        return properties

    def _infer_table_name(self, class_name: str, namespace: str) -> str:
        """Infer table name from class name"""
        # Simple pluralization (could use a library in production)
        if class_name.endswith('y'):
            table_name = class_name[:-1] + 'ies'
        elif class_name.endswith('s'):
            table_name = class_name
        else:
            table_name = class_name + 's'
        return table_name

    def _infer_schema(self, namespace: str) -> str:
        """Infer schema from namespace"""
        if 'AbpIdentity' in namespace or 'Identity' in namespace:
            return 'AbpIdentity'
        elif 'PermissionManagement' in namespace:
            return 'PermissionManagement'
        else:
            return 'public'

    def _build_relationship_graph(self):
        """Build relationship graph from entity properties"""
        for entity_name, entity in self.entities.items():
            for prop in entity.properties:
                if prop.is_foreign_key and prop.referenced_entity:
                    # Check if referenced entity exists
                    if prop.referenced_entity in self.entities:
                        # Many-to-One relationship (child has FK to parent)
                        rel = RelationshipInfo(
                            source_entity=entity_name,
                            target_entity=prop.referenced_entity,
                            relationship_type='many-to-one',
                            source_fk=prop.name,
                            source_navigation=prop.name[:-2] if prop.name.endswith('Id') else prop.name
                        )
                        self.relationships.append(rel)

                        # Check for reverse navigation (parent has collection of children)
                        for child_prop in self.entities[prop.referenced_entity].properties:
                            if child_prop.type == entity_name or (child_prop.type.endswith('ICollection') and entity_name in child_prop.type):
                                if child_prop.name not in [r.source_navigation for r in self.relationships if r.target_entity == prop.referenced_entity]:
                                    rel_reverse = RelationshipInfo(
                                        source_entity=prop.referenced_entity,
                                        target_entity=entity_name,
                                        relationship_type='one-to-many',
                                        target_navigation=prop.name[:-2] if prop.name.endswith('Id') else prop.name
                                    )
                                    self.relationships.append(rel_reverse)

        # Detect many-to-many via join tables
        self._detect_many_to_many()

    def _detect_many_to_many(self):
        """Detect many-to-many relationships"""
        for entity_name, entity in self.entities.items():
            # Check if entity has exactly 2 foreign keys that reference different entities
            fk_properties = [p for p in entity.properties if p.is_foreign_key]

            if len(fk_properties) == 2:
                entity1_fk, entity2_fk = fk_properties
                entity1_name = entity1_fk.referenced_entity
                entity2_name = entity2_fk.referenced_entity

                if entity1_name and entity2_name and entity1_name != entity2_name:
                    # This looks like a join table
                    # Check naming pattern: {Entity1}{Entity2} or {Entity1}{Entity2}s
                    lowercase_name = entity_name.lower()
                    expected_patterns = [
                        f"{entity1_name.lower()}{entity2_name.lower()}",
                        f"{entity2_name.lower()}{entity1_name.lower()}",
                        f"{entity1_name.lower()}{entity2_name.lower()}s",
                        f"{entity2_name.lower()}{entity1_name.lower()}s",
                    ]

                    if any(lowercase_name.startswith(pattern) for pattern in expected_patterns):
                        rel = RelationshipInfo(
                            source_entity=entity1_name,
                            target_entity=entity2_name,
                            relationship_type='many-to-many',
                            join_entity=entity_name,
                            source_fk=entity1_fk.name,
                            target_fk=entity2_fk.name
                        )
                        self.relationships.append(rel)

    def _build_schema_model(self) -> Dict[str, Any]:
        """Build complete schema model"""
        return {
            'entities': {name: asdict(entity) for name, entity in self.entities.items()},
            'relationships': [asdict(rel) for rel in self.relationships],
            'base_classes': {name: [asdict(prop) for prop in props]
                           for name, props in self.base_classes.items()}
        }


class QueryGenerator:
    """Generates PostgreSQL queries based on discovered schema"""

    def __init__(self, schema_model: Dict[str, Any]):
        self.schema = schema_model
        self.entities = schema_model['entities']
        self.relationships = schema_model['relationships']

    def generate_query(self, user_request: str) -> str:
        """Generate PostgreSQL query based on user request"""
        print(f"\n[Q] Generating query for: '{user_request}'")

        # Analyze request to determine target entity
        target_entity = self._identify_target_entity(user_request)

        if not target_entity:
            return self._generate_help_response(user_request)

        # Determine what relationships are needed
        needed_joins = self._identify_joins(target_entity, user_request)

        # Build the query
        query = self._build_select_query(target_entity, needed_joins, user_request)

        return query

    def _identify_target_entity(self, request: str) -> Optional[str]:
        """Identify the main entity from user request"""
        request_lower = request.lower()

        # Try to match entity names
        for entity_name, entity_data in self.entities.items():
            # Check exact name (case-insensitive)
            if entity_name.lower() in request_lower:
                return entity_name
            # Check table name
            if entity_data['table_name'].lower() in request_lower:
                return entity_name
            # Check DisplayName/Name fields if they exist
            for prop in entity_data['properties']:
                if prop['name'].lower() in ['name', 'displayname', 'systemname', 'title']:
                    # This is a naming column, entity is probable
                    pass

        # Default: look for most common entities as heuristics
        common_entities = ['Application', 'Operation', 'Workflow', 'Task', 'User', 'Role']
        for common in common_entities:
            for entity_name in self.entities.keys():
                if common.lower() in entity_name.lower():
                    return entity_name

        return None

    def _identify_joins(self, target_entity: str, request: str) -> List[Dict[str, Any]]:
        """Identify required joins based on request"""
        joins = []
        target_entity_lower = target_entity.lower()

        for rel in self.relationships:
            if rel['source_entity'] == target_entity:
                # Check if target entity appears in request
                if rel['target_entity'].lower() in request.lower():
                    joins.append(rel)
            elif rel['target_entity'] == target_entity:
                joins.append(rel)

        return joins

    def _build_select_query(self, entity_name: str, joins: List[Dict[str, Any]], request: str) -> str:
        """Build SELECT query with joins"""
        entity = self.entities[entity_name]
        table_name = entity['table_name']
        schema = entity['schema']

        # Start building
        sql_lines = []
        sql_lines.append("SELECT")

        # Select main entity columns (exclude large JSON fields for performance)
        main_columns = []
        for prop in entity['properties']:
            col_name = f'"{prop["name"]}"'
            if prop['type'] not in ['JSONB', 'TEXT'] and 'data' not in prop['name'].lower():
                main_columns.append(f'  e."{prop["name"]}"')

        if not main_columns:
            main_columns = ['e.*']

        sql_lines.append(",\n".join(main_columns))

        # Add joined columns
        for join_rel in joins:
            target_entity = join_rel['target_entity']
            target_data = self.entities.get(target_entity)
            if not target_data:
                continue

            # Add commonly useful columns from joined table
            for prop in target_data['properties']:
                if prop['type'] not in ['JSONB', 'TEXT'] and not prop['name'].startswith('Id'):
                    alias = target_entity[:3].lower()
                    sql_lines.append(f',  {alias}."{prop["name"]}" as "{alias}_{prop["name"]}"')

        sql_lines.append(f"FROM {schema}.\"{table_name}\" e")

        # Add JOINs
        for join_rel in joins:
            target_entity = join_rel['target_entity']
            target_data = self.entities.get(target_entity)
            if not target_data:
                continue

            join_type = "JOIN"  # Could be LEFT JOIN based on need
            target_table = f"{target_data['schema']}.\"{target_data['table_name']}\""
            alias = target_entity[:3].lower()

            # Determine join condition
            if join_rel['relationship_type'] == 'many-to-one':
                # Find FK property
                fk_prop = next((p for p in entity['properties']
                              if p['is_foreign_key'] and p.get('referenced_entity') == target_entity), None)
                if fk_prop:
                    join_cond = f'{alias}."{target_data["properties"][0]["name"]}" = e."{fk_prop["name"]}"'
                else:
                    join_cond = f'{alias}."Id" = e."{target_entity}Id"'
            elif join_rel['relationship_type'] == 'many-to-many':
                join_entity = join_rel['join_entity']
                join_data = self.entities.get(join_entity)
                if join_data:
                    join_cond = f'e."Id" = {join_entity[:3].lower()}."{entity_name}Id" AND {alias}."Id" = {join_entity[:3].lower()}."{target_entity}Id"'
                    sql_lines.append(f"JOIN {join_data['schema']}.\"{join_data['table_name']}\" {join_entity[:3].lower()} ON {join_entity[:3].lower()}.\"{entity_name}Id\" = e.\"Id\"")
                    sql_lines.append(f"JOIN {target_table} {alias} ON {alias}.\"Id\" = {join_entity[:3].lower()}.\"{target_entity}Id\"")
                    continue
            else:  # one-to-many
                join_cond = f'{alias}."{entity_name}Id" = e."{target_data["properties"][0]["name"]}"'

            sql_lines.append(f"{join_type} {target_table} {alias} ON {join_cond}")

        # Add WHERE clause with tenant and soft delete filters
        where_clauses = []

        if entity['is_multi_tenant']:
            where_clauses.append('e."TenantId" = @tenantId')

        if entity['is_soft_delete']:
            where_clauses.append('e."IsDeleted" = false')

        # Add entity-specific filters based on request keywords
        # Look for status, stage, or type filters
        for prop in entity['properties']:
            prop_name = prop['name'].lower()
            if any(keyword in prop_name for keyword in ['status', 'stage', 'type', 'state']):
                if 'active' in request.lower() and prop_name in ['isactive', 'active']:
                    where_clauses.append(f'e."{prop["name"]}" = true')
                if 'processing' in request.lower() and 'stage' in prop_name:
                    where_clauses.append(f'e."SystemName" ILIKE \'%processing%\'')

        if where_clauses:
            sql_lines.append("WHERE " + "\n  AND ".join(where_clauses))

        # Add ORDER BY
        if any(p for p in entity['properties'] if p['name'] in ['CreationTime', 'CreatedDate', 'ModifiedDate']):
            sql_lines.append("ORDER BY e.\"CreationTime\" DESC")

        # Add LIMIT for safety
        sql_lines.append("LIMIT @maxResultCount OFFSET @skipCount;")

        return "\n".join(sql_lines)

    def _generate_help_response(self, request: str) -> str:
        """Generate help response when entity not found"""
        available_entities = list(self.entities.keys())[:10]

        return f"""-- Query generation guidance

-- Request: {request}

-- Unable to identify target entity automatically.
-- Available entities in this project:
{chr(10).join(f'--   - {e}' for e in available_entities)}

-- Please refine your request to include an entity name.
-- Examples:
--   "Get all Applications with workflow stages"
--   "Find Operations in processing stage"
--   "Show Users with active roles"
"""


def _sanitize_filename(text: str) -> str:
    """Sanitize text to create a valid filename"""
    # Remove special characters, replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', text)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.strip('_').lower()


def _generate_filename(query: str, target_entity: Optional[str]) -> str:
    """Generate a filename for the SQL query"""
    # Use entity name if discovered
    if target_entity:
        base_name = target_entity
    else:
        # Use first few words of query
        words = query.split()[:4]
        base_name = '_'.join(words) if words else 'query'

    sanitized = _sanitize_filename(base_name)
    timestamp = int(time.time())
    return f"{sanitized}_{timestamp}.sql"


def main():
    parser = argparse.ArgumentParser(description='PostgreSQL Query Generator')
    parser.add_argument('--query', '-q', help='Natural language query to generate SQL for')
    parser.add_argument('--project-root', '-p', default='.',
                       help='Project root directory (default: current directory)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode')
    parser.add_argument('--discover-only', '-d', action='store_true',
                       help='Only perform discovery, output schema to JSON')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')

    args = parser.parse_args()

    # Perform discovery
    discovery = DomainDiscovery(args.project_root)
    schema = discovery.discover()

    if args.discover_only:
        # Output schema model
        output = json.dumps(schema, indent=2, default=str)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"\n[OK] Schema saved to: {args.output}")
        else:
            print(json.dumps(schema, indent=2, default=str))
        return

    # Generate queries
    generator = QueryGenerator(schema)

    if args.interactive:
        print("\n" + "=" * 60)
        print("Interactive Query Generation Mode")
        print("Type 'quit' or 'exit' to leave")
        print("=" * 60 + "\n")

        while True:
            try:
                query_request = input("\n[INPUT] Enter query: ").strip()
                if query_request.lower() in ['quit', 'exit', 'q']:
                    break

                sql = generator.generate_query(query_request)
                print("\n" + sql)
                print("-" * 60)

            except KeyboardInterrupt:
                print("\n")
                break
            except Exception as e:
                print(f"[ERROR] Error: {e}")
    elif args.query:
        sql = generator.generate_query(args.query)

        # Determine output file
        output_file = args.output
        if not output_file:
            # Auto-generate filename in current directory
            target_entity = None
            # Try to identify target entity from the query for a better filename
            entities = list(generator.entities.keys())
            for entity in entities:
                if entity.lower() in args.query.lower():
                    target_entity = entity
                    break
            output_file = _generate_filename(args.query, target_entity)

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql)
        print(f"\n[OK] Query saved to: {output_file}")
    else:
        # Show usage
        parser.print_help()


if __name__ == '__main__':
    main()
