/**

@copyright
<pre>


	Copyright (c) 2014 Institute for Electronic Design Automation, TU Munich

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.


</pre>
@author Marc Greim <marc.greim@mytum.de>

@date November 21, 2014

@version 0.4

*/
/**
	@file

	@brief

	@detail

*/
#ifndef ETISS_INTERFACES_DOT_H
#define ETISS_INTERFACES_DOT_H

#include "etiss/Misc.h"
#include "etiss/ObjectPool.h"
#include "etiss/RefCountedObject.h"
#include "etiss/FixedSizeHashMap.h"

#include <fstream>
#include <unordered_set>
#include <list>
#include <vector>
#include <functional>
#include <unordered_map>
#include <limits>

namespace std
{
template <>
struct hash<std::pair<void const*, void const*> >
{
    std::hash<intptr_t> mh;
    inline size_t operator()(const std::pair<void const*, void const*>  & x) const
    {
        ///TODO check if additional computation needed for a propper hash combination (e.g. FNV) is worth it
        // create a pseudo pointer
        intptr_t ret = ((intptr_t)x.first*13) ^ ((intptr_t)x.second*23) ^ (((intptr_t)x.first>>15)*19) ^ (((intptr_t)x.second>>15)*29);

        return ret;
    }
};
}

namespace etiss
{
namespace interfaces
{

/**
	@attention if an id is a pointer then the pointer must remain valid during the use of that id. otherwise anything may be chosen as an id that doesn't start with "p_"
*/
class Dot
{
public:
    class AttrList
    {
        friend class etiss::interfaces::Dot;
    public:
        std::string label_;
        std::string color_;
    public:
        virtual void print(std::ostream & out ,const std::string & appendedattr);
    };
    class Link;
    class Graph;
    class Node : public AttrList
    {
        friend class etiss::interfaces::Dot;
    private:
        inline Node(Dot * dot,Graph * parent,const std::string & id) : dot_(dot),parent_(parent),id_(id.empty()?(std::string("p_")+etiss::toString((size_t)this)):id)
        {
            if (parent)
                parent->nodes_.insert(this);
            if (dot)
                dot->idmap_.insert(std::make_pair(id_,this));
        }
    public:
        virtual inline ~Node()
        {
            while (!links_.empty())
                delete *links_.begin();
            if (parent_)
                parent_->nodes_.erase(this);
            if (dot_)
                dot_->idmap_.erase(id_);

        }
    public:
        Dot * const dot_;
        Graph * const parent_;
        const std::string id_;
    private:
        std::unordered_set<Link*> links_;
    public:
        inline const std::unordered_set<Link*> & links()
        {
            return links_;
        }
    public:
        virtual inline Graph * asGraph()
        {
            return nullptr;
        }
    public:
        virtual void print(std::ostream & out,std::unordered_set<Link*> & icl);
    };
    class Link : public AttrList
    {
        friend class etiss::interfaces::Dot;
    private:
        Link(Node * src,Node * dst) : src_(src),dst_(dst)
        {
            if (src)
                src->links_.insert(this);
            if (dst)
                dst->links_.insert(this);
        }
    public:
        virtual inline ~Link()
        {
            if (src_)
                src_->links_.erase(this);
            if (dst_)
                dst_->links_.erase(this);
        }
    public:
        Node * const src_;
        Node * const dst_;
    public:
        virtual void print(std::ostream & out);
    };
    class Graph : public Node
    {
        friend class etiss::interfaces::Dot;
    private:
        inline Graph(Dot * dot,Graph * parent) : Node(dot,parent,"") {}
    public:
        virtual inline ~Graph()
        {
            while (!nodes_.empty())
                delete (*nodes_.begin());
            for (auto iter = dot_->graphs_.begin(); iter != dot_->graphs_.end(); ++iter)
            {
                if (*iter == this)
                {
                    dot_->graphs_.erase(iter);
                    break;
                }
            }
        }
    public:
        virtual inline Graph * asGraph()
        {
            return this;
        }
    private:
        std::unordered_set<Node*> nodes_;
    public:
        inline const std::unordered_set<Node*> & nodes()
        {
            return nodes_;
        }
    public:
        virtual void print(std::ostream & out,std::unordered_set<Link*> & icl);
    };

private:
    std::list<Graph*> graphs_;
    std::unordered_map<std::string,Node *> idmap_;
public:
    ~Dot();
    inline const std::list<Graph*> graphs()
    {
        return graphs_;
    }

    Graph * createG(std::string name = "");
    Graph * createG(Graph * parent,std::string name = "");
    Node * createN(Graph *,const std::string & id,std::string name = "");
    inline Node * pcreateN(Graph *g,const void * id,std::string name = "")
    {
        return createN(g,id?(std::string("p_")+etiss::toString((size_t)this)):"",name);
    }
    Link * createE(Node * src,Node * dst,std::string name = "");

    Node * find(const std::string & id);

    /**
    	travel/creates sub graphs with the given labels until i find/creates a node for the lase label. ids will be auto created if neccessary
    	@attention if labels are not unique then the selected graphs/nodes are undefined
    */
    Node * lopenN(const std::list<std::string> & labelpath);

public:
    virtual void print(std::ostream & out);

};

namespace dot
{

class ValueOperationTraceGraph
{
public:
    class Link;
    class Node
    {
    public:
        inline Node() : id(0) {}
        const void * id;
        std::list<Link*> links;
    };
    class Link
    {
    public:
        inline Link() : dst(0) {}
        std::string color;
        std::string label;
        Node * dst;
    };
public:
    void defineNode(const void * id,const std::string & name);
    void undefineNode(const void *id);

    Link * link(const void *src,const void *dst);

    void flush(std::ofstream & out,const std::string & graph);

private:

    void filterTmp(Node * start,Node * tmp,bool hideedge,const std::string & alabels,std::ofstream & out,std::unordered_set<Node*> & nnl,std::unordered_set<std::pair<const void *,const void*> > & dependencies,std::unordered_set<Node*> & declared);

    Node start;
    std::unordered_map<const void*,Node*> currentnodes_;
    std::unordered_map<const void*,Node*> currentdstnodes_;
    std::unordered_map<const void*,std::string> nodes_;
};

class ValueOperationTraceGraphStreamer
{
public:
    class Link;
    class Node //: public etiss::RefCountedObject<etiss::ObjectPool<Node> >
    {
        friend class Link;
        friend class ValueOperationTraceGraphStreamer;
    public:
        static const double Nan;
    public:
        inline Node(const void * id) : id(id),color(0),cluster(0),time(Nan),weight(Nan),links_in_(links_in),links_out_(links_out),attrMap(0) {}
		~Node();
        const void * const id;
        const char * color;
        const char * cluster;
        double time;
        double weight;
        //std::name name; // name is stored in nodes_ map to prevent unneccessary copies;
        void attrToString(std::ostream & out);
        const std::unordered_set<Link*> & links_in_;
        const std::unordered_set<Link*> & links_out_;
        void setAttr(const std::string & name,const std::string & value);
    private:
        std::unordered_set<Link*> links_in;
        std::unordered_set<Link*> links_out;
        std::map<std::string,std::string> * attrMap;
    };
    class Link
    {
    public:
        static const size_t label_size = 256;
        inline Link(Node * src,Node *dst) : color(""),taken(true),src(src),dst(dst)
        {
            if ((src == 0)||(dst==0))
                throw "error";
            if (src==dst)
                throw "loop error";
            label[0] = 0;
        }
        const char * color;
        char label[label_size];
        void setLabel(const char *);
        bool taken;
        void attrToString(std::ostream & out);
        Node * const src;
        Node * const dst;
    };
public:
    ValueOperationTraceGraphStreamer(const std::string & file,const std::string & depfile);
    ~ValueOperationTraceGraphStreamer();
    void defineNode(const void * id,const std::string & name);
    void undefineNode(const void *id);

    void link(const void * dst,std::initializer_list<const void *> sources,const char * label = 0);

    void close();

    void flush();

    const std::unordered_set<std::pair<const void *,const void*> > & staticDependencies() const;

    bool enable_default_graph_streaming_; ///< set to false to disable the streaming of variable dependencies over time. in that case only the static dependencies are streamed and custWritePath is used

private:

    void writePath();
    void traverse(Node * n);//,std::unordered_set<Node*> & nodes); // debug loop detection
    etiss::ExpandingNativeStack<Link*,1000> path;

    Node* openDestNode(const void * const dst,Node * & cleanup);
    Node* openSourceNode(const void * const src);

    uint64_t nnodeid_;
    etiss::FixedSizeHashMap<Node *,uint64_t,etiss::pointerHash<const void> > nodeToTmpId_;
    uint64_t curdstnodeid_;
    etiss::FixedSizeHashMap<const void*,Node*,etiss::pointerHash<const void> > currentnodes_;
    //std::unordered_map<const void*,Node*,std::hash<const void*>, std::equal_to<const void*>,etiss::ObjectPool<std::pair<const void * const,Node*> > > currentnodes_;
    etiss::FixedSizeHashMap<const void*,std::string,etiss::pointerHash<const void> > nodes_;


    std::unordered_set<std::pair<const void *,const void*> > dependencies_;

    std::ofstream out;
    std::ofstream depout;
public:
    std::function<void(Node *)> setCurrentNodeAttr;
    std::function<void(Link *,Node * /*dst*/,Node * const * /*sources*/,size_t /*sources_count*/,std::initializer_list<const void *> & /*raw sources*/,const char * /*op*/)> setCurrentLinkAttr;
    std::function<void(Link *,const etiss::ExpandingNativeStack<Link*,1000> & )> setMetaLinkAttr;
    std::function<void(const etiss::ExpandingNativeStack<Link*,1000> & )> custWritePath;
    std::function<bool(const etiss::ExpandingNativeStack<Link*,1000> & )> hidePath;


private:
    etiss::ObjectPool<Node> node_alloc_;
    etiss::ObjectPool<Link> link_alloc_;

    char out_buf[256*256];
    char depout_buf[256*256];

    bool closed_;

};

class VariableDependencyGraph
{
private:
    std::unordered_map<const void *,std::unordered_set<const void*> ,std::hash<const void*>, std::equal_to<const void*>,etiss::ObjectPool<std::pair<const void * const,std::unordered_set<const void*> > > > tmp_;
    std::unordered_map<const void *,std::string,std::hash<const void*>, std::equal_to<const void*>,etiss::ObjectPool<std::pair<const void * const,std::string > > > names_;
    std::unordered_set<std::pair<const void*,const void*> ,std::hash<std::pair<const void*,const void*> >, std::equal_to<std::pair<const void*,const void*> >,etiss::ObjectPool<std::pair<const void * const,const void* const > > > deps_;
public:
    VariableDependencyGraph();
    inline void declare(const void * const id,const std::string & name)
    {
        names_.insert(std::make_pair(id,name));
        tmp_.erase(id);
    }
    inline void deleted(const void * const id)
    {
        tmp_.erase(id);
        names_.erase(id);
    }
    void link(const void * dst,const std::initializer_list<const void *> & sources);

    void write(
        std::ostream & out,
        const std::string & graphname,
        std::function<bool(const void* /*src*/,const void * /*dst*/,std::string & /*color*/)> filterOutCon = [](const void *,const void *,std::string & )
    {
        return false;
    },
    std::function<void(const void * /*id*/,std::string & /*color*/)> nodeattr = [](const void *,std::string &) {}
    );

public:


#ifdef TRACEABLEFIED_H_
    /// @attention any id must be a valid pointer to TraceableFieldBase; implemented in TraceableField.cpp
    void tf_write(const std::string & filename);
#endif

};


}




} // namespace interfaces
} // namespace etiss

#endif // ETISS_INTERFACES_DOT_H
