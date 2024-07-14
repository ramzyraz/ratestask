from ..queries import GET_CHILD_SLUGS, GET_PORT_CODES

# finds all slugs including child slugs
def get_all_child_slugs(conn, parent_slug):
    child_slugs = [parent_slug]

    try:
        with conn.cursor() as cursor:
            # Recursive function to fetch child slugs
            def fetch_child_slugs(slug):
                cursor.execute(GET_CHILD_SLUGS, (slug,))
                results = cursor.fetchall()

                # Recursively fetch all child slugs 
                for result in results:
                    child_slugs.append(result[0])
                    fetch_child_slugs(result[0])
            
            fetch_child_slugs(parent_slug)
    except Exception as e:
        print(f"Error fetching child slugs: {e}")
    
    return child_slugs

# Finds the port of the given slug
def get_port_codes(conn, slug):
    try:
        with conn.cursor() as cursor:
            cursor.execute(GET_PORT_CODES, (slug,))
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching port code: {e}")
        return []